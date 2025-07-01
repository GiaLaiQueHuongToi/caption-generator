#!/bin/bash

# Quick fix script for PyTorch version conflicts
echo "🔧 PyTorch Version Fix Script"
echo "============================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

echo ""
echo "🔍 Current PyTorch status:"
python3 -c "
try:
    import torch
    print(f'✅ PyTorch {torch.__version__} is installed')
except ImportError:
    print('❌ PyTorch not installed')
"

echo ""
echo "🔧 Fixing PyTorch installation..."

# Uninstall existing conflicting versions
echo "📤 Removing existing PyTorch installations..."
pip uninstall torch torchaudio torchvision -y

# Install compatible PyTorch version
echo "📥 Installing compatible PyTorch..."
if python3 -c "import platform; exit(0 if platform.system() == 'Darwin' and 'arm' in platform.machine().lower() else 1)"; then
    # Apple Silicon Mac
    echo "🍎 Detected Apple Silicon - installing optimized PyTorch"
    pip install torch torchaudio
else
    # Other systems - use CPU version for compatibility
    echo "💻 Installing CPU-optimized PyTorch"
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Install WhisperX
echo "📥 Installing/Updating WhisperX..."
pip install whisperx

# Test installation
echo ""
echo "🧪 Testing installation..."
python3 -c "
try:
    import torch
    print(f'✅ PyTorch {torch.__version__} - OK')
    import torchaudio
    print(f'✅ TorchAudio {torchaudio.__version__} - OK')
    import whisperx
    print('✅ WhisperX - OK')
    print('🎉 All dependencies working!')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PyTorch fix completed successfully!"
    echo "🚀 You can now run: ./start.sh"
else
    echo ""
    echo "❌ Fix failed. Check TROUBLESHOOTING.md for more options."
    exit 1
fi
