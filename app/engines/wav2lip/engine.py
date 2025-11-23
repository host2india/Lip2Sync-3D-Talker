# app/engines/wav2lip/engine.py
import os
import uuid
import subprocess
from typing import Dict, Optional

from app.engines.wav2lip.utils import (
    save_uploaded_bytes,
    ensure_outputs_dir,
    merge_audio_video_if_needed,
)

class Wav2LipEngine:
    """
    Production-ready Wav2Lip engine (Video + Audio -> lip-synced video).
    - Expects model infer.py in model_path (default: Wav2Lip folder)
    - Works with 'workspace' param (use '.' for local testing, '/workspace' in Pod)
    - Writes canonical output to <workspace>/outputs/video_sync.mp4
    """

    def __init__(self, model_path: str = "Wav2Lip", workspace: Optional[str] = None):
        # workspace: if environment variable WORKSPACE set, use that, else default to current directory
        env_ws = os.environ.get("WORKSPACE")
        if workspace is None:
            workspace = env_ws if env_ws else "."
        self.model_path = model_path
        self.workspace = workspace
        self.temp_dir = os.path.join(self.workspace, "temp")
        self.outputs_dir = os.path.join(self.workspace, "outputs")
        os.makedirs(self.temp_dir, exist_ok=True)
        ensure_outputs_dir(self.outputs_dir)

    def run(self, video_bytes: bytes, audio_bytes: Optional[bytes] = None) -> Dict:
        job_id = str(uuid.uuid4())

        # Paths
        video_in = os.path.join(self.temp_dir, f"{job_id}_in_video.mp4")
        audio_in = None
        if audio_bytes:
            audio_in = os.path.join(self.temp_dir, f"{job_id}_in_audio.wav")
        merged_video = os.path.join(self.temp_dir, f"{job_id}_merged.mp4")
        job_output = os.path.join(self.outputs_dir, f"{job_id}_video_sync.mp4")
        final_output = os.path.join(self.outputs_dir, "video_sync.mp4")  # canonical

        # Save uploaded files
        save_uploaded_bytes(video_bytes, video_in)
        if audio_bytes:
            save_uploaded_bytes(audio_bytes, audio_in)

        # If audio provided separately, merge it into the video for stability,
        # otherwise infer.py can accept separate --audio param; but we'll pass the merged video.
        if audio_in:
            try:
                merge_audio_video_if_needed(video_in, audio_in, merged_video)
                face_input = merged_video
            except Exception as e:
                return {"status": "error", "details": f"ffmpeg merge failed: {e}"}
        else:
            face_input = video_in

        # Validate model paths
        infer_script = os.path.join(self.model_path, "infer.py")
        checkpoint = os.path.join(self.model_path, "checkpoints", "wav2lip.pth")
        if not os.path.exists(infer_script):
            return {"status": "error", "details": f"infer.py not found at {infer_script}"}
        if not os.path.exists(checkpoint):
            return {"status": "error", "details": f"checkpoint not found at {checkpoint}"}

        # Build command
        # We use --face <video> and --audio <audio> if audio provided separately,
        # but since we merged above we can simply pass the merged video and the same audio file to be safe.
        command = [
            "python3",
            infer_script,
            "--checkpoint_path", checkpoint,
            "--face", face_input,
        ]
        if audio_in:
            command += ["--audio", audio_in]
        else:
            # If the input video already has audio, infer will extract it. No --audio param needed.
            pass
        command += ["--outfile", job_output]

        # Run inference
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return {"status": "error", "details": f"inference failed: {e}"}

        # Move/rename to canonical final filename (overwrite if exists)
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.rename(job_output, final_output)
        except Exception:
            return {"status": "success", "output_path": job_output}

        return {"status": "success", "output_path": final_output}
