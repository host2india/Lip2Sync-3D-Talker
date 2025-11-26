#!/bin/bash
set -e

echo "=============================="
echo "⬇️ DOWNLOADING ALL MODELS"
echo "=============================="

MODEL_DIR="models"
SADTALKER_DIR="$MODEL_DIR/sadtalker"
WAV2LIP_DIR="$MODEL_DIR/wav2lip/checkpoints"

mkdir -p "$SADTalker_DIR"
mkdir -p "$WAV2LIP_DIR"

echo "📦 Downloading Wav2Lip models..."
gdown --fuzzy "https://drive.google.com/file/d/1NWV…/view" -O "$WAV2LIP_DIR/wav2lip.pth"

gdown --fuzzy "https://drive.google.com/file/d/1s3F…/view" -O "$WAV2LIP_DIR/s3fd.pth"

echo "📦 Downloading SadTalker models..."

gdown --fuzzy "https://drive.google.com/drive/folders/1CV-a6KimmhZcW92sN9bWAeSYidBJYIgc" -O "$SADTalker_DIR" --folder

gdown --fuzzy "https://drive.google.com/drive/folders/1QugS7P7-8x37WfLmRMZf-fykZXaYZLcw" -O "$SADTalker_DIR/BFM_Fitting" --folder

echo "✅ All models downloaded."
