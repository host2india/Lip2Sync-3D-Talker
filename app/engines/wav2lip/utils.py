# app/engines/wav2lip/utils.py
import os
import subprocess

def save_uploaded_bytes(data: bytes, path: str) -> str:
    with open(path, "wb") as f:
        f.write(data)
    return path

def ensure_outputs_dir(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def merge_audio_video_if_needed(video_in: str, audio_in: str, out_path: str):
    """
    Use ffmpeg to merge audio + video into out_path.
    Requires ffmpeg present in PATH.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", video_in,
        "-i", audio_in,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        "-map", "0:v:0",
        "-map", "1:a:0",
        out_path
    ]
    subprocess.run(cmd, check=True)
    return out_path
