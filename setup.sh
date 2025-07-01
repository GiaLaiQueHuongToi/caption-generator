#!/bin/bash

# Video Caption Generator Setup Script
echo "🎥 Setting up Video Caption Generator..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python version: $PYTHON_VERSION"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed."
    echo "Please install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi

echo "✅ FFmpeg is installed"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies with fallback options
echo "📥 Installing dependencies..."
if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️ Main requirements failed, trying flexible version..."
    if pip install -r requirements-flexible.txt; then
        echo "✅ Flexible requirements installed successfully"
    else
        echo "❌ Both requirement files failed. Trying manual installation..."
        echo "📦 Installing PyTorch first..."
        pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
        echo "📦 Installing WhisperX..."
        pip install whisperx
        echo "📦 Installing FastAPI and other dependencies..."
        pip install fastapi uvicorn[standard] python-multipart requests aiofiles python-dotenv Pillow numpy moviepy
        echo "✅ Manual installation complete"
    fi
fi

# Create temp directory
echo "📁 Creating temp directory..."
mkdir -p temp

# Copy environment file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
    echo "Please configure your .env file as needed."
else
    echo "✅ Environment file already exists"
fi

# Download WhisperX model (this might take a while on first run)
echo "🤖 Testing WhisperX model download..."
python3 -c "
try:
    import whisperx
    print('WhisperX imported successfully')
    # Note: Model will be downloaded on first API call
except ImportError as e:
    print(f'Warning: WhisperX import failed: {e}')
    print('This might be resolved when running the actual API')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the API server:"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📖 API documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧪 Test the API with:"
echo "   curl -X POST \"http://localhost:8000/generate-captioned-video\" \\"
echo "     -F \"file=@your_video.mp4\" \\"
echo "     -F \"font_size=28\" \\"
echo "     -F \"font_color=yellow\" \\"
echo "     -F \"position=bottom\""
echo ""
echo "❓ If you encounter issues, check TROUBLESHOOTING.md"
