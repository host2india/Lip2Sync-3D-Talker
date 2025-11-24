import os
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Tuple

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def make_temp_dir(base: str = "/tmp/sadtalker") -> str:
    ensure_dir(base)
    d = os.path.join(base, str(uuid.uuid4()))
    ensure_dir(d)
    return d

def cleanup_dir(path: str):
    try:
        shutil.rmtree(path)
    except Exception:
        pass

def run_ffmpeg_extract_audio(video_path: str, out_wav: str) -> None:
    cmd = ["ffmpeg","-y","-i",video_path,"-ar","16000","-ac","1",out_wav]
    subprocess.run(cmd, check=True)

def run_ffmpeg_combine(frames_pattern: str, audio_path: str, out_path: str, fps: int = 25) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", frames_pattern,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-strict", "-2",
        out_path,
    ]
    subprocess.run(cmd, check=True)
