# app/engines/wav2lip_single_image/engine.py

import os
import uuid
import subprocess
from typing import Dict, Optional

from app.engines.wav2lip_single_image.utils import (
    save_uploaded_bytes,
    ensure_outputs_dir,
    merge_audio_video_if_needed,
)

class Wav2LipSingleImageEngine:
    """
    Single-image Wav2Lip engine.
    Creates a short video from the image, merges audio (if provided),
    runs Wav2Lip inference, and outputs final talking video.
    """

    def __init__(self, model_path: str = "models/wav2lip", workspace: Optional[str] = None):
        # Detect workspace automatically (RunPod sets WORKSPACE)
        env_ws = os.environ.get("WORKSPACE")
        if workspace is None:
            workspace = env_ws if env_ws else "."

        self.model_path = model_path
        self.workspace = workspace

        # Create working folders
        self.temp_dir = os.path.join(self.workspace, "temp_single_image")
        self.outputs_dir = os.path.join(self.workspace, "outputs")
        os.makedirs(self.temp_dir, exist_ok=True)
        ensure_outputs_dir(self.outputs_dir)

    def run(self, image_bytes: bytes, audio_bytes: Optional[bytes] = None) -> Dict:
        job_id = str(uuid.uuid4())

        # File paths
        img_in = os.path.join(self.temp_dir, f"{job_id}_image.png")
        audio_in = os.path.join(self.temp_dir, f"{job_id}_audio.wav") if audio_bytes else None

        # Intermediate outputs
        still_video = os.path.join(self.temp_dir, f"{job_id}_still.mp4")
        merged_input = os.path.join(self.temp_dir, f"{job_id}_merged.mp4")

        model_output = os.path.join(self.outputs_dir, f"{job_id}_model.mp4")
        final_output = os.path.join(self.outputs_dir, "single_image.mp4")

        # Save incoming files
        try:
            save_uploaded_bytes(image_bytes, img_in)
            if audio_bytes:
                save_uploaded_bytes(audio_bytes, audio_in)
        except Exception as e:
            return {"status": "error", "details": f"Failed to save uploaded files: {e}"}

        # ------------------------------------------------------------------
        # Create still-video (image → 60s H.264 640x640)
        # ------------------------------------------------------------------
        try:
            cmd_still = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img_in,
                "-c:v", "libx264",
                "-t", "60",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=640:640",
                still_video
            ]
            subprocess.run(cmd_still, check=True)
        except subprocess.CalledProcessError as e:
            return {"status": "error", "details": "FFmpeg failed creating still video"}

        # ------------------------------------------------------------------
        # Merge audio if available
        # ------------------------------------------------------------------
        if audio_bytes:
            try:
                merge_audio_video_if_needed(still_video, audio_in, merged_input)
                face_input = merged_input
            except Exception as e:
                return {"status": "error", "details": f"Audio merge failed: {e}"}
        else:
            face_input = still_video

        # ------------------------------------------------------------------
        # Validate model files
        # ------------------------------------------------------------------
        infer_script = os.path.join(self.model_path, "infer.py")
        checkpoint = os.path.join(self.model_path, "checkpoints", "wav2lip.pth")

        if not os.path.exists(infer_script):
            return {"status": "error", "details": f"infer.py missing at {infer_script}"}
        if not os.path.exists(checkpoint):
            return {"status": "error", "details": f"wav2lip checkpoint missing at {checkpoint}"}

        # ------------------------------------------------------------------
        # Run Wav2Lip inference
        # ------------------------------------------------------------------
        command = [
            "python3",
            infer_script,
            "--checkpoint_path", checkpoint,
            "--face", face_input,
            "--outfile", model_output,
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return {"status": "error", "details": f"Inference failed: returncode {e.returncode}"}

        # ------------------------------------------------------------------
        # Final move
        # ------------------------------------------------------------------
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.rename(model_output, final_output)
        except Exception:
            # If rename fails, return model_output instead
            return {"status": "success", "output_path": model_output}

        return {"status": "success", "output_path": final_output}
