from fastapi import FastAPI, UploadFile, File
from .wav2lip_engine import synthesize_lips
from .sadtalker_engine import synthesize_talking
import uvicorn

app = FastAPI(title="Lip2Sync API")

@app.get("/")
def root():
    return {"status":"ok","service":"Lip2Sync-Server"}

@app.post("/wav2lip")
async def wav2lip(file: UploadFile = File(...)):
    # placeholder: save file -> call engine
    content = await file.read()
    out_path = "uploads/output_wav2lip.mp4"
    return {"message":"received", "filename": file.filename, "output": out_path}

@app.post("/sadtalker")
async def sadtalker(file: UploadFile = File(...)):
    content = await file.read()
    out_path = "uploads/output_sadtalker.mp4"
    return {"message":"received", "filename": file.filename, "output": out_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
