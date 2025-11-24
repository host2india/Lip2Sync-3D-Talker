# 🚀 Lip2Sync-3D-Talker — Google Colab Setup Guide  
**One-click GPU setup for 3D Talking Avatar Engine**

This page provides a clean, well-structured guide for using **Lip2Sync-3D-Talker** on Google Colab, including:

- 🔥 One-Click Install Script  
- 📥 Auto-download all model files  
- ⚙️ GPU-accelerated SadTalker + Lip2Sync engine  
- 🎬 Run inference instantly

---

## ⭐ Quick Start (One-Click)

Click this button to open Colab instantly:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/host2india/Lip2Sync-3D-Talker/blob/main/Colab_AutoSetup.py)

---

## ⚡ One Cell Setup (Copy & Run in Colab)

```python
#===========================================================
# 🚀 Lip2Sync-3D-Talker — One-Click Auto Setup (COLAB)
#===========================================================
import os, gdown

REPO = "https://github.com/host2india/Lip2Sync-3D-Talker.git"
CKPT = "models/sadtalker/checkpoints"
WAV2CKPT = "models/wav2lip/checkpoints"

os.makedirs(CKPT, exist_ok=True)
os.makedirs(WAV2CKPT, exist_ok=True)

print("🔥 Cloning repository...")
!git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
%cd Lip2Sync-3D-Talker

print("⚙️ Installing requirements...")
!pip install -r models/sadtalker_src/requirements3d.txt || pip install -r requirements.txt

def down(id, out):
    if not os.path.exists(out):
        gdown.download(f"https://drive.google.com/uc?id={id}", out, quiet=False)
    else:
        print(f"✔️ Exists: {out}")

#======== SadTalker 3D Models ========#
FILES = {
    "epoch_20.pth": "1Yj-s_mOOi0Cze3hMewGfYi1NhvUr9tus",
    "audo2exp_00300-model.pth": "1FEeNXMmsgUDGAH2LkIOoXtJSWG9jln1V",
    "audio2pose_00140-model.pth": "1-127XXF3jtT39dsQCzA7zrHq_ltbAuP4",
    "mapping_00109-model.pth.tar": "1T7Q1gCB-wwlZhym5bX45AWxFOPV-fZYi",
    "mapping_00229-model.pth.tar": "1H4cIAn-URt8OEh7ykJW-38AzRpz4bSIM",
    "epoch_00190.pth.tar": "1B6-Sark54byn8d9HeAvjqXrcuiY8hxuP",
    "hubert_soft.pt": "1Xqhfsr3ZXUlogrwNiFg9Y734cpbrm4zK",
    "GFV.pth": "11rhboV2IJZi1q6t34kfvuwxSmWChOuJQ",
    "facevid2vid_00189-model.pth.tar": "1BHpU7tErSxtqdNpoA2aqqxR5BnrB46Jx",
    "shape_predictor_68_face_landmarks.dat": "18Xiw0JDNe5b0yc0lJ6XJoMb2O7WZ9Pvi",
}

print("📥 Downloading 3D Checkpoints...")
for fname, gid in FILES.items():
    down(gid, f"{CKPT}/{fname}")

#======== Wav2Lip Optional ========#
WAV = {
    "s3fd.pth": "1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbv1",
    "wav2lip.pth": "12Mma_hL4uQMnnm19NDIT5jQ51MdSiOye",
    "wav2lip_gan.pth": "1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC",
}

print("📥 Downloading Optional Wav2Lip Models...")
for fname, gid in WAV.items():
    down(gid, f"{WAV2CKPT}/{fname}")

print("\n🎉 Setup Complete — You can now run the engine!")
🧪 Run Inference (Colab)
python
Copy code
from app.engines.sadtalker.engine import SadTalkerEngine

engine = SadTalkerEngine(device="cuda")

video = engine.infer_from_files(
    "input_image.png",
    "input_audio.wav"
)

video
Output video will be displayed directly in Colab.

📁 Folder Structure in Colab
powershell
Copy code
Lip2Sync-3D-Talker/
│── app/
│── models/
│   └── sadtalker/
│       └── checkpoints/
│── outputs/
│── Colab_AutoSetup.py
└── README.md
🟧 Tips for Fast Performance
Tip	Benefit
Use T4 GPU	5–20× faster
Convert audio to 16-bit WAV	More stable mouth movement
Use clear face images	Better 3D reconstruction

❗ Troubleshooting
❌ “CUDA not available”
➡️ Runtime → Change Runtime Type → GPU

❌ 404 Download error
Google Drive link expired — update Drive IDs

❌ dlib build error
Colab installer already avoids dlib; you are safe 👍

💬 Credits
Balu & Captain 

SadTalker authors

GFPGAN, RealESRGAN teams

Lip2Sync engine stack

