# Vision Dockerfile — GroundingDINO + SAM2 + Depth Anything
# Base image: PyTorch with CUDA 11.8 support
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy==1.24.4 \
    opencv-python==4.8.1.78 \
    Pillow==10.1.0 \
    transformers==4.36.2 \
    supervision==0.18.0

# Copy application code into the container
COPY . /app

# Default command when container starts
CMD ["python", "vision_node.py"]