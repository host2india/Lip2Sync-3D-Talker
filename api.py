from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# === ROUTE IMPORTS ===
from app.routes.wav2lip_single_image import router as wav2lip_single_image_router
from app.routes.wav2lip import router as wav2lip_router

# === CREATE APP FIRST ===
app = FastAPI(title="Lip2Sync API Server", version="1.0")

# === CORS (optional but recommended) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ROUTES (order does not matter once app exists) ===
app.include_router(wav2lip_single_image_router, prefix="/api")
app.include_router(wav2lip_router, prefix="/api")


# === HEALTH CHECK ===
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Lip2Sync Server Running",
        "routes": [
            "/api/sync/single_image",
            "/api/sync/wav2lip",
        ],
    }


