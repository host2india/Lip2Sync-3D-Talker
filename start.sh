#!/bin/bash
set -e

apt update && apt install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    build-essential \
    libgl1-mesa-glx

cd /workspace/app

pip install --upgrade pip
pip install -r requirements.txt

bash download_models.sh

uvicorn api:app --host 0.0.0.0 --port 8000
