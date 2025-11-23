import os
import yaml
import time
from pathlib import Path
from fastapi import UploadFile
from PIL import Image

from .utils import make_temp_dir, cleanup_dir, run_ffmpeg_combine, ensure_dir

class SadTalkerEngine:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.device = self.cfg.get("options", {}).get("device", "cuda")
        self.fps = self.cfg.get("options", {}).get("fps", 25)
        self.output_dir = self.cfg.get("options", {}).get("output_dir", "app/engines/sadtalker/output")
        ensure_dir(self.output_dir)

        self.model = None
        self._load_models()

    def _load_models(self):
        print("[SadTalker] Model loading stub (replace with actual SadTalker loading).")

    def infer_from_files(self, image_path: str, audio_path: str, out_name: str = None) -> str:
        t0 = time.time()
        tmp = make_temp_dir(self.cfg.get("options", {}).get("temp_dir", "/tmp/sadtalker"))
        try:
            frames_pattern = os.path.join(tmp, "%05d.png")

            # Placeholder frame generation
            im = Image.open(image_path).convert("RGB")
            for i in range(1, 6):
                im.resize((256, 256)).save(os.path.join(tmp, f"{i:05d}.png"))

            # Output video
            if out_name is None:
                out_name = f"sadtalker_out_{int(time.time())}.mp4"

            out_path = os.path.join(self.output_dir, out_name)
            run_ffmpeg_combine(frames_pattern, audio_path, out_path, fps=self.fps)

            print(f"[SadTalker] Done in {time.time() - t0:.2f}s -> {out_path}")
            return out_path

        finally:
            cleanup_dir(tmp)

    async def infer_from_uploads(self, image_file: UploadFile, audio_file: UploadFile) -> str:
        tmp = make_temp_dir()
        try:
            image_path = os.path.join(tmp, "input_image.png")
            audio_path = os.path.join(tmp, "input_audio.wav")

            with open(image_path, "wb") as f:
                f.write(await image_file.read())

            with open(audio_path, "wb") as f:
                f.write(await audio_file.read())

            return self.infer_from_files(image_path, audio_path)

        finally:
            cleanup_dir(tmp)
