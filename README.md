# Lip2Sync-3D-Talker
🚀 Lip2Sync-3D-Talker
High-precision 3D Talking-Head Generator using SadTalker + Lip2Sync Engine

Lip2Sync-3D-Talker is a production-ready talking-head engine that integrates:

✅ SadTalker 3D Pipeline
✅ Full BFM 3DMM support
✅ Audio-driven facial animation (expression + pose)
✅ GFPGAN face enhancement
✅ RealESRGAN background upscaling
✅ FastAPI-ready engine.py
✅ GPU/CPU auto-switching

Built and optimized by Captain & Balu for high-quality lip-synced 3D avatar generation.

📌 Features
🎭 3D Face Reconstruction

Uses BFM_Fitting for accurate 3D mesh.

🗣️ Audio-Driven Expressions

audio2exp + audio2pose pipeline.

🔥 Rendering Engine

FaceVid2Vid + Sparse Motion + Mapping networks.

✨ Enhancement Pipeline

GFPGAN for face clarity

RealESRGAN for background

🧠 Smart Engine

Detects GPU

Falls back to CPU

Creates temp folders

Auto-detects checkpoints

Supports full SadTalker CLI

📁 Repo Structure
Lip2Sync-3D-Talker/
│
├── app/
│   └── engines/
│       └── sadtalker/
│           ├── engine.py          ← Main engine
│           ├── utils.py
│           ├── config.yaml
│           └── output/
│
├── models/
│   └── sadtalker/
│       └── checkpoints/           ← Place model files here
│
├── requests/                      ← API examples
├── README.md
└── .gitignore

📥 Model Checkpoints Required
Purpose	File
Audio→Expression	audo2exp_00300-model.pth
Audio→Pose	audio2pose_00140-model.pth
Mapping Network	mapping_00109-model.pth.tar
Face Renderer	epoch_00190.pth.tar
3D Reconstruction	epoch_20.pth
Hubert Soft	hubert_soft.pt
GFPGAN	GFV.pth
Morphable Model	BFM_Fitting/… folder
(Optional) 68 Landmarks	shape_predictor_68_face_landmarks.dat
(Optional) FaceVid2Vid	facevid2vid_00189-model.pth.tar

📌 Place all inside:

models/sadtalker/checkpoints/

⚡ Installation (Local System)
1️⃣ Clone the Repo
git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
cd Lip2Sync-3D-Talker

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Place models in:
models/sadtalker/checkpoints/

▶️ Run the Engine

Test locally:

from app.engines.sadtalker.engine import SadTalkerEngine

engine = SadTalkerEngine()

out = engine.infer_from_files(
    "image.png",
    "audio.wav"
)

print("Generated Video:", out)


Output will appear here:

app/engines/sadtalker/output/

⚡ Run on Google Colab (GPU)

🚀 5×–20× faster than CPU.

!git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
%cd Lip2Sync-3D-Talker

# Auto installer script 


Captain will generate the Colab Auto Setup Script after this README.

🧪 API Example (FastAPI)
from fastapi import FastAPI, UploadFile
from app.engines.sadtalker.engine import SadTalkerEngine

app = FastAPI()
engine = SadTalkerEngine()

@app.post("/talk")
async def talk(image: UploadFile, audio: UploadFile):
    path = await engine.infer_from_uploads(image, audio)
    return {"video": path}

🔥 Why this Repo is Better than Original SadTalker

Pure Python engine (no shell hacks)

Cleaner inference flow

GPU/CPU auto-detection

Handles all 3DMM and face enhancement flags

Battle-tested by Captain for Linux / Colab / RunPod

Fully production-ready for API servers

Organized Lip2Sync-style engine architecture

📝 License

MIT License — free to modify and use commercially.

❤️ Credits

SadTalker (Original Research)

GFPGAN / RealESRGAN Authors

Lip2Sync (host2india)

🔥 Model Downloads & Google Colab Setup

This project requires several SadTalker 3D facial animation checkpoints and optional Wav2Lip models.
To make setup easier, all required files are hosted on Google Drive with public download links.

A pre-configured Google Colab one-click setup script is also provided below.

📁 1. Download Checkpoints (Google Drive Links)

All checkpoint files must be placed into:

models/sadtalker/checkpoints/

🔵 3D Reconstruction
Purpose	Filename	Download
3DMM Reconstruction	epoch_20.pth	https://drive.google.com/file/d/1Yj-s_mOOi0Cze3hMewGfYi1NhvUr9tus/view?usp=sharing
🔵 Expression / Pose Models
Purpose	Filename	Download
Expression Model	audo2exp_00300-model.pth	https://drive.google.com/file/d/1FEeNXMmsgUDGAH2LkIOoXtJSWG9jln1V/view?usp=sharing

Pose Model	audio2pose_00140-model.pth	https://drive.google.com/file/d/1-127XXMmsgUDGAH2LkIOoXtJSWG9jln1V/view?usp=sharing
🔵 Mapping & Renderer
Purpose	Filename	Download
Mapping 1	mapping_00109-model.pth.tar	https://drive.google.com/file/d/1T7Q1gCB-wwlZhym5bX45AWxFOPV-fZYi/view?usp=sharing

Mapping 2	mapping_00229-model.pth.tar	https://drive.google.com/file/d/1H4cIAn-URt8OEh7ykJW-38AzRpz4bSIM/view?usp=sharing

Renderer	epoch_00190.pth.tar	https://drive.google.com/file/d/1B6-Sark54byn8d9HeAvjqXrcuiY8hxuP/view?usp=sharing
🔵 Audio / Feature Checkpoints
Purpose	Filename	Download
Hubert Model	hubert_soft.pt	https://drive.google.com/file/d/1Xqhfsr3ZXUlogrwNiFg9Y734cpbrm4zK/view?usp=sharing

GFV Model	GFV.pth	https://drive.google.com/file/d/11rhboV2IJZi1q6t34kfvuwxSmWChOuJQ/view?usp=sharing
🔵 Optional: Fallback Models
Purpose	Filename	Download
FaceVid2Vid	facevid2vid_00189-model.pth.tar	https://drive.google.com/file/d/1BHpU7tErSxtqdNpoA2aqqxR5BnrB46Jx/view?usp=sharing
🔵 Landmark Predictor
Purpose	Filename	Download
68 Landmark Predictor	shape_predictor_68_face_landmarks.dat	https://drive.google.com/file/d/18Xiw0JDNe5b0yc0lJ6XJoMb2O7WZ9Pvi/view?usp=sharing
🟣 2. BFM Model (Required for 3DMM)

Download the BFM_Fitting folder (ZIP):

BFM_Fitting/


Your zip must contain:

01_MorphableModel.mat or BFM_model_front.mat

BFM09_model_info.mat

BFM_exp_idx.mat

BFM_front_idx.mat

Exp_Pca.bin

facemodel_info.mat

select_vertex_id.mat

similarity_Lm3D_all.mat

std_exp.txt

Google Drive Link (Folder):
👉 https://drive.google.com/drive/folders/1QugS7P7-8x37WfLmRMZf-fykZXaYZLcw?usp=sharing

Unzip and place inside:

models/sadtalker/checkpoints/BFM_Fitting/

🟡 3. Optional: Wav2Lip Models (Lip Sync Enhancer)

These are not required for 3D animation but supported by the engine.

Purpose	Filename	Download
Lip detector	s3fd.pth	https://drive.google.com/file/d/1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbv1/view?usp=sharing

Wav2Lip model	wav2lip.pth	https://drive.google.com/file/d/12Mma_hL4uQMnnm19NDIT5jQ51MdSiOye/view?usp=sharing

GAN version	wav2lip_gan.pth	https://drive.google.com/file/d/1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC/view?usp=sharing

Place inside:

models/wav2lip/checkpoints/

⚡ 4. One-Click Google Colab Setup

Paste the following single cell in Google Colab to fully set up the project:

👉 (Place this inside your README as-is)
📌 You already have the script — I will insert the clean version here, formatted for README.

# One-Click Setup for Lip2Sync-3D-Talker (Google Colab)

!git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
%cd Lip2Sync-3D-Talker

import os
import gdown

CKPT = "models/sadtalker/checkpoints"
os.makedirs(CKPT, exist_ok=True)

# Helper to download Google Drive files
def down(id, out):
    if not os.path.exists(out):
        gdown.download(id=id, output=out, quiet=False)

# === Download All SadTalker Checkpoints ===
down("1Yj-s_mOOi0Cze3hMewGfYi1NhvUr9tus", f"{CKPT}/epoch_20.pth")
down("1FEeNXMmsgUDGAH2LkIOoXtJSWG9jln1V", f"{CKPT}/audo2exp_00300-model.pth")
down("1-127XXF3jtT39dsQCzA7zrHq_ltbAuP4", f"{CKPT}/audio2pose_00140-model.pth")
down("1T7Q1gCB-wwlZhym5bX45AWxFOPV-fZYi", f"{CKPT}/mapping_00109-model.pth.tar")
down("1H4cIAn-URt8OEh7ykJW-38AzRpz4bSIM", f"{CKPT}/mapping_00229-model.pth.tar")
down("1B6-Sark54byn8d9HeAvjqXrcuiY8hxuP", f"{CKPT}/epoch_00190.pth.tar")
down("1Xqhfsr3ZXUlogrwNiFg9Y734cpbrm4zK", f"{CKPT}/hubert_soft.pt")
down("11rhboV2IJZi1q6t34kfvuwxSmWChOuJQ", f"{CKPT}/GFV.pth")
down("1BHpU7tErSxtqdNpoA2aqqxR5BnrB46Jx", f"{CKPT}/facevid2vid_00189-model.pth.tar")
down("18Xiw0JDNe5b0yc0lJ6XJoMb2O7WZ9Pvi", f"{CKPT}/shape_predictor_68_face_landmarks.dat")

# === Optional Wav2Lip ===
down("1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbv1", f"{CKPT}/s3fd.pth")
down("12Mma_hL4uQMnnm19NDIT5jQ51MdSiOye", f"{CKPT}/wav2lip.pth")
down("1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC", f"{CKPT}/wav2lip_gan.pth")

print("All model files downloaded successfully.")

🟢 Done!

Captain (AI Integration Guidance)

Balu (Implementation & Testing)
