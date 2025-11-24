# Lip2Sync-3D-Talker
🚀 Lip2Sync-3D-Talker

High-precision Talking Head Generation using SadTalker + Lip2Sync 3D pipeline.

🔥 Features

Full 3DMM (BFM_Fitting) support

High-fidelity face movement using SadTalker

Face enhancement (GFPGAN)

Background upscaling (RealESRGAN)

Pure Python & FastAPI backend

GPU/CPU auto-detection

Clean engine integration inside Lip2Sync architecture

📦 Folder Structure (Clean Version)
Lip2Sync-3D-Talker/
│
├── app/
│   └── engines/
│       └── sadtalker/
│           ├── engine.py
│           ├── utils.py
│           ├── config.yaml
│           └── output/
│
├── models/
│   └── sadtalker/
│       └── checkpoints/   (user downloads models manually)
│
├── requests/              (example API calls)
├── README.md
└── .gitignore

🛠 Installation (Local System)
1. Clone repo
git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
cd Lip2Sync-3D-Talker

2. Install requirements
pip install -r requirements.txt

3. Download SadTalker models

Place them inside:

models/sadtalker/checkpoints/


Required:

Purpose	File
Audio → Expression	audo2exp_00300-model.pth
Audio → Pose	audio2pose_00140-model.pth
3D Reconstruction	epoch_20.pth
Mapping Network	mapping_00109-model.pth.tar
GFPGAN	GFV.pth
BFM Fitting	BFM_Fitting/ (folder)
🚀 Run Engine Test (Python)
from app.engines.sadtalker.engine import SadTalkerEngine

e = SadTalkerEngine()

out = e.infer_from_files("image.png", "audio.wav")

print("Video:", out)
