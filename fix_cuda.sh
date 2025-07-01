#!/bin/bash

# CUDA/cuDNN Fix Script for Video Caption Generator

echo "🔧 CUDA/cuDNN Issues Fix Script"
echo "=============================="

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ] && [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "🔍 Checking current setup..."

# Check CUDA availability
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU devices: {torch.cuda.device_count()}')
else:
    print('No CUDA devices detected')
"

echo ""
echo "🛠️ Applying fixes..."

# Method 1: Force CPU usage via environment variable
echo "📝 Setting environment variable to force CPU usage..."
export CUDA_VISIBLE_DEVICES=""
echo "CUDA_VISIBLE_DEVICES=" >> .env
echo "✅ Environment configured for CPU-only"

# Method 2: Reinstall CPU-only PyTorch
echo ""
echo "📦 Reinstalling CPU-only PyTorch libraries..."
pip uninstall torch torchaudio -y
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Method 3: Reinstall WhisperX
echo ""
echo "📦 Reinstalling WhisperX..."
pip uninstall whisperx -y
pip install whisperx

# Test the fix
echo ""
echo "🧪 Testing the fix..."
python3 -c "
import torch
print(f'✅ PyTorch {torch.__version__} - CPU only')
print(f'CUDA available: {torch.cuda.is_available()}')

try:
    import whisperx
    print('✅ WhisperX imported successfully')
except ImportError as e:
    print(f'❌ WhisperX import failed: {e}')

import os
if os.getenv('CUDA_VISIBLE_DEVICES') == '':
    print('✅ CUDA_VISIBLE_DEVICES set to force CPU usage')
else:
    print('⚠️ CUDA_VISIBLE_DEVICES not set')
"

echo ""
echo "🎉 CUDA fix complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart your API server: ./start.sh"
echo "   2. Test with: python3 test_api_quick.py"
echo ""
echo "💡 The API will now run in CPU-only mode, which is slower but more compatible."
