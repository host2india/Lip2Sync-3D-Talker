#!/bin/bash
set -e

echo "=============================="
echo "🚀 STARTING LIP2SYNC SERVER..."
echo "=============================="

# Activate workspace
cd /workspace/Lip2Sync-3D-Talker || cd /workspace/app || true

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "🎯 Ensuring model directory exists..."
mkdir -p models/sadtalker
mkdir -p models/wav2lip/checkpoints

echo "⬇️ Downloading missing models..."
chmod +x download_models.sh
./download_models.sh

echo "🔧 Applying performance patches..."
export PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=0

echo "🚀 Launching FastAPI server..."
uvicorn api:app \
    --host 0.0.0.0 \
    --port ${APP_PORT:-8000} \
    --workers 1 \
    --timeout-keep-alive 120 \
    --no-access-log
