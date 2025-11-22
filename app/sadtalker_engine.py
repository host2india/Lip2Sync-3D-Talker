import os, subprocess
from pathlib import Path

MODELS_DIR = Path("models/sadtalker")
SAD_SCRIPT = Path("sadtalker/inference_sadtalker.py")  # if you add real SadTalker, place script here

def ffmpeg_image_audio_loop(image_path, audio_path, out_path):
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

def synthesize_talking(source_image, input_audio, output_path="uploads/sadtalker_output.mp4"):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if SAD_SCRIPT.exists():
        cmd = [
            "python", str(SAD_SCRIPT),
            "--driven_audio", str(input_audio),
            "--source_image", str(source_image),
            "--result_dir", str(output.parent)
        ]
        subprocess.run(cmd, check=True)
        # assume the script writes a result in result_dir; return the first mp4 there
        for p in output.parent.iterdir():
            if p.suffix.lower() == ".mp4":
                return str(p)
        return str(output)

    # fallback to ffmpeg image+audio loop
    return ffmpeg_image_audio_loop(source_image, input_audio, output_path)
