# Troubleshooting Guide

## Common Installation Issues

### 1. PyTorch Version Conflicts

**Error:** `Could not find a version that satisfies the requirement torch==2.1.0`

**Solutions:**

```bash
# Option 1: Use flexible requirements
pip install -r requirements-flexible.txt

# Option 2: Install PyTorch first from official source
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
# Then install other requirements
pip install -r requirements.txt

# Option 3: Let pip choose compatible versions
pip install torch torchaudio
pip install whisperx
pip install fastapi uvicorn python-multipart
```

### 2. WhisperX API Compatibility Issues

**Error:** `TranscriptionOptions.__init__() missing 5 required positional arguments`

This occurs when there's a version mismatch between WhisperX versions with different APIs.

**Solutions:**

```bash
# Option 1: Check and test compatibility
python3 check_whisperx.py

# Option 2: Install specific compatible version
pip uninstall whisperx -y
pip install whisperx==3.1.1

# Option 3: Update to latest version
pip install whisperx --upgrade

# Option 4: Manual fix
pip uninstall whisperx torch torchaudio -y
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install whisperx
```

### 3. WhisperX Installation Issues

**Error:** Various WhisperX compilation errors

**Solutions:**

```bash
# Install system dependencies first (Ubuntu/Debian)
sudo apt update
sudo apt install build-essential python3-dev

# For macOS
xcode-select --install

# Install with specific versions
pip install torch==2.4.1 torchaudio==2.4.1
pip install whisperx==3.1.1
```

### 4. FFmpeg Not Found

**Error:** `FFmpeg not found`

**Solutions:**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# Check installation
ffmpeg -version
```

### 5. CUDA Issues

**Error:** CUDA-related errors even with CPU-only setup

**Solutions:**

```bash
# Force CPU-only PyTorch
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Or set environment variable
export CUDA_VISIBLE_DEVICES=""
```

### 6. Memory Issues

**Error:** Out of memory during processing

**Solutions:**

- Use smaller WhisperX model in `.env`:
  ```
  WHISPERX_MODEL=base
  # or
  WHISPERX_MODEL=small
  ```
- Reduce video resolution before processing
- Ensure sufficient RAM (4GB+ recommended)

### 7. Permission Issues

**Error:** Permission denied errors

**Solutions:**

```bash
# Make scripts executable
chmod +x setup.sh start.sh test_examples.sh

# Fix temp directory permissions
mkdir -p temp
chmod 755 temp
```

### 8. Port Already in Use

**Error:** `Address already in use: 8000`

**Solutions:**

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### 9. CUDA/cuDNN Library Issues

**Error:** `Could not load library libcudnn_ops_infer.so.8` or similar CUDA library errors

This occurs when the system tries to use GPU acceleration but CUDA libraries are missing or incompatible.

**Quick Fix (Force CPU-only):**

```bash
# Set environment variable to force CPU usage
export CUDA_VISIBLE_DEVICES=""

# Or restart the API with CPU-only PyTorch
pip uninstall torch torchaudio -y
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Restart the API
./start.sh
```

**Permanent Solutions:**

```bash
# Option 1: Add to your .env file
echo "CUDA_VISIBLE_DEVICES=" >> .env

# Option 2: Install proper CUDA libraries (Ubuntu/Debian)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get install libcudnn8

# Option 3: Use CPU-only for all ML libraries
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install whisperx --no-deps
pip install transformers datasets librosa soundfile
```

## Alternative Installation Methods

### Method 1: Step-by-step Installation

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install PyTorch first
pip install torch torchaudio

# 4. Install WhisperX
pip install whisperx

# 5. Install FastAPI
pip install fastapi uvicorn[standard] python-multipart

# 6. Install remaining dependencies
pip install requests aiofiles python-dotenv Pillow numpy moviepy
```

### Method 2: Conda Installation

```bash
# Create conda environment
conda create -n caption-gen python=3.9
conda activate caption-gen

# Install PyTorch via conda
conda install pytorch torchaudio -c pytorch

# Install other packages
pip install whisperx fastapi uvicorn python-multipart
pip install requests aiofiles python-dotenv Pillow numpy moviepy
```

### Method 3: Docker (Bypass Local Issues)

```bash
# Build and run with Docker
docker build -t caption-generator .
docker run -p 8000:8000 caption-generator
```

## Testing Installation

```bash
# Test Python imports
python3 -c "import torch; print('PyTorch:', torch.__version__)"
python3 -c "import whisperx; print('WhisperX: OK')"
python3 -c "import fastapi; print('FastAPI: OK')"

# Test FFmpeg
ffmpeg -version

# Test full project
python3 validate_project.py
```

## Environment-Specific Notes

### Apple Silicon (M1/M2)

```bash
# Use MPS backend for acceleration
pip install torch torchaudio

# Set environment
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### Windows

```bash
# Use conda for easier dependency management
conda install pytorch torchaudio -c pytorch
pip install whisperx fastapi uvicorn
```

### Linux Servers (No GUI)

```bash
# Install headless dependencies
sudo apt install python3-dev build-essential
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Getting Help

If you continue to have issues:

1. Check the specific error message
2. Verify Python version (3.8+)
3. Ensure FFmpeg is installed
4. Try the flexible requirements file
5. Use Docker as a fallback
6. Check WhisperX GitHub issues for known problems
