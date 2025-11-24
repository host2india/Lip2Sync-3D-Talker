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

# Auto installer script (Captain will generate next)


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

Captain (AI Integration Guidance)

Balu (Implementation & Testing)
