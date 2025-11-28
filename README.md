# 🎭 Lip2Sync-3D-Talker  
### **High-Precision 3D Talking-Head Generator (SadTalker + Lip2Sync Engine)**  
Built by **Captain & Balu**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/host2india/Lip2Sync-3D-Talker/blob/main/Colab_AutoSetup.ipynb)

---

## 🚀 Overview  
**Lip2Sync-3D-Talker** is a **production-grade 3D talking-avatar generation engine** integrating:

- ✅ SadTalker 3DMM pipeline  
- ✅ Full **BFM_Fitting** 3D reconstruction  
- ✅ Audio-driven animation (expression + pose)  
- ✅ GFPGAN facial enhancement  
- ✅ RealESRGAN background enhancement  
- ✅ Lip2Sync-style FastAPI engine  
- ✅ Clean Python architecture & GPU/CPU auto-switching  

It is **faster, cleaner, and more stable** than the original SadTalker repository.

---

## 🏗 System Architecture

Lip2Sync 3D Architecture <img width="1024" height="1536" alt="ChatGPT Image Nov 24, 2025, 11_24_36 PM" src="https://github.com/user-attachments/assets/06a8c66f-1efc-4b1b-bb39-a393023cbf42" />


---

## 🎬 Sample Output

> *This is a placeholder preview — replace with real sample later.*

![Sample Output](sample_output.gif)

---

## 📁 Repository Structure

Lip2Sync-3D-Talker/
│
├── app/
│ └── engines/
│ └── sadtalker/
│ ├── engine.py
│ ├── utils.py
│ ├── config.yaml
│ └── output/
│
├── models/
│ └── sadtalker/
│ └── checkpoints/ # Place all model files here
│
├── requests/ # Example API requests
├── templates/
├── uploads/
└── README.md


---

# 📥 **Model Downloads (Google Drive)**  
**All required files must be placed here:**  
models/sadtalker/checkpoints/


---

## 🔵 **1. Core 3D Reconstruction Models**

| Purpose | Filename | Download |
|--------|----------|----------|
| 3DMM Reconstruction | **epoch_20.pth** | https://drive.google.com/file/d/1Yj-s_mOOi0Cze3hMewGfYi1NhvUr9tus/view?usp=sharing |
| Expression Model | **audo2exp_00300-model.pth** | https://drive.google.com/file/d/1FEeNXMmsgUDGAH2LkIOoXtJSWG9jln1V/view?usp=sharing |
| Pose Model | **audio2pose_00140-model.pth** | https://drive.google.com/file/d/1-127XXF3jtT39dsQCzA7zrHq_ltbAuP4/view?usp=sharing |

---

## 🟣 **2. Mapping + Rendering**

| Purpose | Filename | Link |
|--------|----------|------|
| MappingNet v1 | **mapping_00109-model.pth.tar** | https://drive.google.com/file/d/1T7Q1gCB-wwlZhym5bX45AWxFOPV-fZYi/view?usp=sharing |
| MappingNet v2 | **mapping_00229-model.pth.tar** | https://drive.google.com/file/d/1H4cIAn-URt8OEh7ykJW-38AzRpz4bSIM/view?usp=sharing |
| Renderer | **epoch_00190.pth.tar** | https://drive.google.com/file/d/1B6-Sark54byn8d9HeAvjqXrcuiY8hxuP/view?usp=sharing |

---

## 🟡 **3. Audio / Feature Models**

| Purpose | Filename | Link |
|--------|----------|------|
| Hubert Soft | **hubert_soft.pt** | https://drive.google.com/file/d/1Xqhfsr3ZXUlogrwNiFg9Y734cpbrm4zK/view?usp=sharing |
| GFPGAN Face Enhancer | **GFV.pth** | https://drive.google.com/file/d/11rhboV2IJZi1q6t34kfvuwxSmWChOuJQ/view?usp=sharing |

---

## 🔴 **4. Optional Fallbacks**

| Purpose | Filename | Link |
|--------|----------|------|
| FaceVid2Vid | **facevid2vid_00189-model.pth.tar** | https://drive.google.com/file/d/1BHpU7tErSxtqdNpoA2aqqxR5BnrB46Jx/view?usp=sharing |
| 68 Landmarks | **shape_predictor_68_face_landmarks.dat** | https://drive.google.com/file/d/18Xiw0JDNe5b0yc0lJ6XJoMb2O7WZ9Pvi/view?usp=sharing |

---

## 🟢 **5. BFM_Fitting (Required for 3DMM)**

➡ Download ZIP (folder):  
https://drive.google.com/drive/folders/1QugS7P7-8x37WfLmRMZf-fykZXaYZLcw?usp=sharing

Extract **inside**:

models/sadtalker/checkpoints/BFM_Fitting/

Must contain:

- 01_MorphableModel.mat  
- BFM09_model_info.mat  
- BFM_exp_idx.mat  
- BFM_front_idx.mat  
- Exp_Pca.bin  
- facemodel_info.mat  
- select_vertex_id.mat  
- similarity_Lm3D_all.mat  
- std_exp.txt  

---

## 🟣 **6. Optional Wav2Lip (Lip Enhancer)**

Place inside:

models/wav2lip/checkpoints/


| File | Link |
|------|------|
| s3fd.pth | https://drive.google.com/file/d/1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbv1/view?usp=sharing |
| wav2lip.pth | https://drive.google.com/file/d/12Mma_hL4uQMnnm19NDIT5jQ51MdSiOye/view?usp=sharing |
| wav2lip_gan.pth | https://drive.google.com/file/d/1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC/view?usp=sharing |

---

# ⚡ Local Installation

## 1️⃣ Clone the repo

```bash
git clone https://github.com/host2india/Lip2Sync-3D-Talker.git
cd Lip2Sync-3D-Talker
2️⃣ Install requirements
bash
Copy code
pip install -r requirements.txt
3️⃣ Place model files
bash
Copy code
models/sadtalker/checkpoints/
▶️ Run Engine (Python)
python
Copy code
from app.engines.sadtalker.engine import SadTalkerEngine

engine = SadTalkerEngine(device="cuda")  # or "cpu"

out = engine.infer_from_files(
    "input.png",
    "audio.wav"
)

print("Generated:", out)
Output saved to:

swift
Copy code
app/engines/sadtalker/output/
🌐 FastAPI Example (Production)
python
Copy code
from fastapi import FastAPI, UploadFile
from app.engines.sadtalker.engine import SadTalkerEngine

app = FastAPI()
engine = SadTalkerEngine()

@app.post("/talk")
async def talk(image: UploadFile, audio: UploadFile):
    out = await engine.infer_from_uploads(image, audio)
    return {"video": out}
Start API:

bash
Copy code
uvicorn api:app --host 0.0.0.0 --port 8000
🐳 Docker Usage
bash
Copy code
docker build -t lipsync-talk3d .
docker run --gpus all -p 8000:8000 lipsync-talk3d
⚡ One-Click Colab Setup
Place this inside README as reference:

csharp
Copy code
[Colab Auto Setup Script — already prepared]
(You already have the full cell.)

🛠 Troubleshooting
❌ “CUDA not found”
Your environment has no GPU. Use:

python
Copy code
SadTalkerEngine(device="cpu")
❌ “Missing epoch_20.pth”
Your checkpoint folder is empty. Fix:

bash
Copy code
models/sadtalker/checkpoints/*
❌ dlib install fail (Colab)
Already solved in AutoSetup script.

🧭 Roadmap
 Web UI (Gradio + Custom UI)

 Full TTS → LipSync Pipeline

 Streaming mode (WebSocket)

 Mobile-friendly avatar export

 4K renderer support

❤️ Credits
SadTalker authors

GFPGAN / RealESRGAN

Lip2Sync base system

Captain & Balu (2025)

📜 License
MIT — free for commercial use.
