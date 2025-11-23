# app/routes/wav2lip.py
import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from app.engines.wav2lip.engine import Wav2LipEngine

router = APIRouter()

# Use WORKSPACE env var when running in Pod; locally it will default to "."
workspace_env = os.environ.get("WORKSPACE", ".")
# model path (if your repo contains Wav2Lip folder, use "Wav2Lip")
model_path = os.environ.get("WAV2LIP_MODEL_PATH", "Wav2Lip")

engine = Wav2LipEngine(model_path=model_path, workspace=workspace_env)

@router.post("/sync/wav2lip")
async def sync_wav2lip(video: UploadFile = File(...), audio: UploadFile = File(None)):
    video_bytes = await video.read()
    audio_bytes = await audio.read() if audio else None

    result = engine.run(video_bytes, audio_bytes)
    if result.get("status") == "success":
        return FileResponse(result["output_path"], media_type="video/mp4", filename="video_sync.mp4")
    return JSONResponse({"status": "error", "details": result.get("details", "unknown")}, status_code=500)
