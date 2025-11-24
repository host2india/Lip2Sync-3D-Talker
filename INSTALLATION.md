📘 INSTALLATION.md
Lip2Sync-3D-Talker – Installation & Setup Guide

This guide explains how to install, configure, and run Lip2Sync-3D-Talker on:

✔ Local Linux Laptop / Desktop

✔ Google Colab GPU

✔ Cloud Servers (RunPod / DigitalOcean)

🚀 1. Requirements
System Requirements
Item	Requirement
OS	Ubuntu/Linux recommended
Python	3.9 – 3.10
GPU	Optional — CUDA improves speed 20×
RAM	8GB+ recommended
Disk	10GB recommended
📦 2. Install Dependencies
2.1 Create a Virtual Environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

2.2 Install Python packages
pip install -r requirements.txt


If you encounter missing packages, install manually:

pip install torch torchvision torchaudio
pip install gfpgan realesrgan facexlib

📁 3. Add Required Model Files

Download the following checkpoints manually.

Purpose	File	Required
3D Reconstruction	epoch_20.pth	✔
Expression model	audo2exp_00300-model.pth	✔
Pose model	audio2pose_00140-model.pth	✔
Mapping network	mapping_00109-model.pth.tar	✔
Main renderer	epoch_00190.pth.tar	✔
Hubert model	hubert_soft.pt	✔
GFPGAN	GFV.pth	✔
Morphable model	Entire BFM_Fitting folder	✔
(Optional) FaceVid2Vid	facevid2vid_00189-model.pth.tar	⚠ Optional
(Optional) 68 Landmarks	shape_predictor_68_face_landmarks.dat	⚠ Optional
Place all files here:
models/sadtalker/checkpoints/


Folder example:

models/
 └── sadtalker/
     └── checkpoints/
         ├── epoch_20.pth
         ├── epoch_00190.pth.tar
         ├── audo2exp_00300-model.pth
         ├── audio2pose_00140-model.pth
         ├── mapping_00109-model.pth.tar
         ├── mapping_00229-model.pth.tar
         ├── hubert_soft.pt
         ├── GFV.pth
         ├── BFM_Fitting/
         └── shape_predictor_68_face_landmarks.dat

🎬 4. Run the Engine Locally
Test script:
from app.engines.sadtalker.engine import SadTalkerEngine

engine = SadTalkerEngine()

out = engine.infer_from_files(
    "image.png",
    "audio.wav"
)

print("Generated Output:", out)


Videos will appear in:

app/engines/sadtalker/output/

⚡ 5. Run the API Server

Install FastAPI & uvicorn:

pip install fastapi uvicorn


Start server:

uvicorn api:app --host 0.0.0.0 --port 3000

🤖 6. Run on Google Colab (GPU)

Create a new notebook and paste:

!git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
%cd Lip2Sync-3D-Talker

!pip install -r requirements.txt

# Download checkpoints manually or mount drive


Then run inference using:

from app.engines.sadtalker.engine import SadTalkerEngine
e = SadTalkerEngine(device="cuda")
e.infer_from_files("image.png", "audio.wav")

🛠 7. Troubleshooting
CUDA not used

Ensure device=“cuda” in config.yaml

Check GPU:

import torch
print(torch.cuda.is_available())

Missing checkpoints

Engine will warn:

FileNotFoundError: mapping_00109-model.pth.tar


→ means model file missing.

Slow inference

CPU mode is 10×–25× slower

Use Google Colab GPU for speed

🎯 8. Recommended Usage

Run inference on Colab GPU

Use this repo to package your engine

Integrate into a backend through FastAPI
