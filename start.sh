#!/bin/bash
echo "🚀 Starting Lip2Sync 3D Talker API..."

# Activate workspace
cd /workspace

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
