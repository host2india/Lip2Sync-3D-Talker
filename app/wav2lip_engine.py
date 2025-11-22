import os, subprocess, shutil
from pathlib import Path

MODELS_DIR = Path("models/wav2lip")
WAV2LIP_SCRIPT = Path("wav2lip/inference.py")  # if you add real inference here, engine will call it

def ffmpeg_merge_image_audio(image_path, audio_path, out_path):
    # Make a simple video from the image + audio (loop image, add audio)
    # uses ffmpeg, expects it to be installed on the system
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(out_path)
    ]
    subprocess.run(cmd, check=True)
    return str(out_path)

def synthesize_lips(input_video_path, input_audio_path, output_path="uploads/wav2lip_output.mp4"):
    """
    Prefer real inference script: wav2lip/inference.py
    If it's not present, fallback to a simple ffmpeg image+audio merge.
    - If `input_video_path` is an image (jpg/png) it will use image fallback.
    - If it's a video and real inference is missing, we will copy video and replace audio.
    """
    input_video = Path(input_video_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # If real inference exists, call it (expects an API similar to Wav2Lip repo)
    if WAV2LIP_SCRIPT.exists():
        cmd = [
            "python", str(WAV2LIP_SCRIPT),
            "--checkpoint_path", str(MODELS_DIR / "wav2lip.pth"),
            "--face", str(input_video_path),
            "--audio", str(input_audio_path),
            "--outfile", str(output)
        ]
        subprocess.run(cmd, check=True)
        return str(output)

    # Fallback behavior:
    # If provided a video, replace its audio using ffmpeg
    suffix = input_video.suffix.lower()
    if suffix in [".jpg", ".jpeg", ".png", ".webp"]:
        return ffmpeg_merge_image_audio(input_video, input_audio_path, output)
    else:
        # replace audio of the input video (quick fallback)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_video),
            "-i", str(input_audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            str(output)
        ]
        subprocess.run(cmd, check=True)
        return str(output)
