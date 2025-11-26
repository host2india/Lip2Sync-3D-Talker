# ---------------------------------------------------------
# Lip2Sync 3D Talker - GPU Dockerfile (SadTalker + GFPGAN + ESRGAN)
# ---------------------------------------------------------

FROM runpod/pytorch:3.10-py3.10-cuda12.1.1-devel

ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------------------------------------
# Install Linux dependencies
# ---------------------------------------------------------
RUN apt-get update && apt-get install -y \
    git ffmpeg wget curl unzip libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
# Create workspace
# ---------------------------------------------------------
WORKDIR /workspace

# ---------------------------------------------------------
# Copy project files (Dockerfile folder → container)
# ---------------------------------------------------------
COPY . /workspace

# ---------------------------------------------------------
# Install Python dependencies
# ---------------------------------------------------------
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# ---------------------------------------------------------
# Download models (SadTalker + GFPGAN + ESRGAN)
# ---------------------------------------------------------
RUN chmod +x download_models.sh && bash download_models.sh

# ---------------------------------------------------------
# Make start.sh runnable
# ---------------------------------------------------------
RUN chmod +x start.sh

# ---------------------------------------------------------
# Expose API ports
# ---------------------------------------------------------
EXPOSE 8000

# ---------------------------------------------------------
# Run server
# ---------------------------------------------------------
CMD ["/workspace/start.sh"]
