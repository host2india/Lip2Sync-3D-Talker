# Wav2Lip Standard ENGINE (video_sync.mp4 output)

### 🔥 Module 1 — Video + Audio → Lip-Synced Video

This engine performs **standard Wav2Lip lip-syncing**:

- Input:
  - **MP4 video** (face video)
  - **Audio** (wav or mp3)
- Output:
  - `video_sync.mp4` (final processed video)

### 📌 Features
- Stable 60fps lip-sync workflow  
- Auto-merges video & audio before inference (ffmpeg)  
- Production-compatible folder structure  
- Works locally and in RunPod GPU  
- Workspace-aware (uses `WORKSPACE=/workspace` in pod)

### 🔧 Paths
- Canonical output:
<workspace>/outputs/video_sync.mp4

diff
Copy code
- Temporary files:
<workspace>/temp/<job_id>_...

markdown
Copy code

### 🛠 Inference Script
The engine calls:
- `Wav2Lip/infer.py`
- Checkpoint:
Wav2Lip/checkpoints/wav2lip.pth

shell
Copy code

### 📡 API Route
POST /api/sync/wav2lip

yaml
Copy code

### 🧪 Upload Fields
- `video` → mp4 video  
- `audio` → wav/mp3 audio  

### ✔ Output
Returns the synced `video_sync.mp4` as a downloadable stream.

---

This module is the **primary** Wav2Lip implementation used for full video-to-audio lip sync.
