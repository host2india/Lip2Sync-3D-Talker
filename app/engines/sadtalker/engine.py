# app/engines/sadtalker/engine.py
import os
import sys
import yaml
import time
import shlex
import logging
import subprocess
import shutil
import glob
import importlib
from pathlib import Path
from fastapi import UploadFile

from .utils import make_temp_dir, cleanup_dir, run_ffmpeg_combine, ensure_dir

log = logging.getLogger("sadtalker_engine")
logging.basicConfig(level=logging.INFO)


def _is_package_available(pkg_name: str) -> bool:
    try:
        importlib.import_module(pkg_name)
        return True
    except Exception:
        return False


class SadTalkerEngine:
    def __init__(self, config_path: str = None):
        # load config
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)

        # device selection from config
        self.device = self.cfg.get("options", {}).get("device", "cuda")

        # fps and output
        self.fps = int(self.cfg.get("options", {}).get("fps", 25))
        self.output_dir = str(
            self.cfg.get("options", {}).get("output_dir", "app/engines/sadtalker/output")
        )
        ensure_dir(self.output_dir)

        # checkpoints directory
        self.ckpt_dir = Path(
            os.path.expanduser(
                self.cfg
                .get("options", {})
                .get("ckpt_dir",
                     str(Path(__file__).resolve().parents[3] / "models/sadtalker/checkpoints"))
            )
        )
        log.info(f"Checkpoint dir set to: {self.ckpt_dir}")

        # major checkpoints
        self.mapping   = self.ckpt_dir / "mapping_00229-model.pth.tar"
        self.renderer  = self.ckpt_dir / "epoch_00190.pth.tar"
        self.hubert    = self.ckpt_dir / "hubert_soft.pt"
        self.gfv       = self.ckpt_dir / "GFV.pth"

        # log missing (optional)
        for p in (self.mapping, self.renderer, self.hubert, self.gfv):
            if not p.exists():
                log.debug(f"(Optional) checkpoint missing: {p}")

        # SadTalker source path
        self.sadtalker_src = Path(
            self.cfg.get("options", {}).get(
                "src_dir",
                str(Path(__file__).resolve().parents[3] / "models/sadtalker_src")
            )
        )
        log.info(f"SadTalker source dir: {self.sadtalker_src}")

        # BFM
        self.bfm_folder = self.ckpt_dir / "BFM_Fitting"
        self.bfm_model_front = self.bfm_folder / "BFM_model_front.mat"
        self.bfm_model_01 = self.bfm_folder / "01_MorphableModel.mat"

        self.use_3dmm = False
        if self.bfm_folder.exists():
            if self.bfm_model_front.exists() or self.bfm_model_01.exists():
                self.use_3dmm = True
                chosen = "BFM_model_front.mat" if self.bfm_model_front.exists() else "01_MorphableModel.mat"
                log.info(f"3DMM ENABLED — BFM detected: {chosen}")
            else:
                log.warning("BFM_Fitting folder exists but MAT files missing.")
        else:
            log.info("No BFM_Fitting folder — 3DMM disabled.")

        # enhancers
        self.has_gfpgan = _is_package_available("gfpgan")
        self.has_realesrgan = _is_package_available("realesrgan")

        if self.has_gfpgan:
            log.info("GFPGAN available.")
        if self.has_realesrgan:
            log.info("RealESRGAN available.")

    def _build_subprocess_cmd(self, image_path: str, audio_path: str, result_dir: str, tmpdir: str):
        """Build command matching new SadTalker CLI."""
        inference_py = self.sadtalker_src / "inference.py"
        if not inference_py.exists():
            raise RuntimeError(f"inference.py missing: {inference_py}")

        cmd = [sys.executable, str(inference_py)]

        # core args
        cmd += ["--driven_audio", audio_path]
        cmd += ["--source_image", image_path]
        cmd += ["--checkpoint_dir", str(self.ckpt_dir)]
        cmd += ["--result_dir", result_dir]
        cmd += ["--preprocess", "full"]

        # DEVICE LOGIC
        use_cpu_flag = False

        # config says CPU
        if self.device.lower() == "cpu":
            use_cpu_flag = True
        else:
            # try GPU
            try:
                import torch
                if not torch.cuda.is_available():
                    log.warning("CUDA requested but not available — using CPU.")
                    use_cpu_flag = True
            except:
                use_cpu_flag = True

        if use_cpu_flag:
            cmd += ["--cpu"]
        else:
            log.info("GPU mode ENABLED — running on CUDA")

        # BFM
        if self.use_3dmm:
            cmd += ["--bfm_folder", str(self.bfm_folder)]
            chosen = "BFM_model_front.mat" if self.bfm_model_front.exists() else "01_MorphableModel.mat"
            cmd += ["--bfm_model", chosen]

        # enhancers
        if self.has_gfpgan:
            cmd += ["--enhancer", "gfpgan"]
        if self.has_realesrgan:
            cmd += ["--background_enhancer", "realesrgan"]

        return cmd

    def _find_output_video(self, result_dir: str):
        candidates = sorted(glob.glob(os.path.join(result_dir, "*.mp4")))
        if candidates:
            return candidates[0]
        candidates = sorted(glob.glob(os.path.join(result_dir, "**", "*.mp4"), recursive=True))
        if candidates:
            return candidates[0]
        return None

    def infer_from_files(self, image_path: str, audio_path: str, out_name: str = None) -> str:
        t0 = time.time()
        tmp = make_temp_dir(self.cfg.get("options", {}).get("temp_dir", "/tmp/sadtalker"))
        try:
            if out_name is None:
                out_name = f"sadtalker_{int(time.time())}.mp4"
            out_path = os.path.join(self.output_dir, out_name)

            result_dir = os.path.join(tmp, "results")
            ensure_dir(result_dir)

            cmd = self._build_subprocess_cmd(image_path, audio_path, result_dir, tmp)
            log.info("Running SadTalker subprocess:\n" + " ".join(shlex.quote(x) for x in cmd))

            proc = subprocess.run(
                cmd, cwd=str(self.sadtalker_src),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False
            )
            out = proc.stdout.decode(errors="ignore")
            log.info("SadTalker subprocess finished:\n" + out)

            found = self._find_output_video(result_dir)
            if found:
                shutil.move(found, out_path)
                log.info(f"SadTalker produced output: {out_path}")
                return out_path

            # fallback: frames
            for root, dirs, files in os.walk(tmp):
                frames = sorted([f for f in files if f.endswith(".png")])
                if len(frames) >= 2:
                    pattern = os.path.join(root, "%05d.png")
                    run_ffmpeg_combine(pattern, audio_path, out_path, fps=self.fps)
                    if os.path.exists(out_path):
                        return out_path

            raise RuntimeError("SadTalker inference failed to produce output.")

        finally:
            cleanup_dir(tmp)
            log.info(f"Total inference time: {time.time() - t0:.2f}s")

    async def infer_from_uploads(self, image_file: UploadFile, audio_file: UploadFile) -> str:
        tmp = make_temp_dir()
        try:
            image_path = os.path.join(tmp, "input_image" + Path(image_file.filename).suffix)
            audio_path = os.path.join(tmp, "input_audio" + Path(audio_file.filename).suffix)

            with open(image_path, "wb") as f:
                f.write(await image_file.read())
            with open(audio_path, "wb") as f:
                f.write(await audio_file.read())

            return self.infer_from_files(image_path, audio_path)
        finally:
            pass
