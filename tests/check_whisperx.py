#!/usr/bin/env python3
"""
WhisperX compatibility checker and fixer
"""

import sys
import subprocess

def check_whisperx_version():
    """Check WhisperX version and API compatibility"""
    try:
        import whisperx
        print(f"✅ WhisperX version: {whisperx.__version__ if hasattr(whisperx, '__version__') else 'unknown'}")
        return True
    except ImportError:
        print("❌ WhisperX not installed")
        return False

def test_whisperx_api():
    """Test WhisperX API compatibility"""
    try:
        import whisperx
        import torch
        
        print("🧪 Testing WhisperX API compatibility...")
        
        # Test model loading
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisperx.load_model("base", device)
        print("✅ Model loading works")
        
        # Test transcription with minimal audio
        import numpy as np
        dummy_audio = np.zeros(16000)  # 1 second of silence
        
        try:
            # Try new API first
            result = model.transcribe(
                dummy_audio,
                batch_size=16,
                language=None,
                multilingual=True,
                max_new_tokens=448,
                clip_timestamps="0,10",
                hallucination_silence_threshold=None,
                hotwords=None
            )
            print("✅ New WhisperX API detected and working")
            return "new"
        except TypeError as e:
            if "missing" in str(e) or "unexpected" in str(e):
                # Try old API
                result = model.transcribe(
                    dummy_audio,
                    batch_size=16,
                    language=None
                )
                print("✅ Old WhisperX API detected and working")
                return "old"
            else:
                raise e
                
    except Exception as e:
        print(f"❌ WhisperX API test failed: {e}")
        return None

def fix_whisperx_version():
    """Fix WhisperX version issues"""
    print("🔧 Attempting to fix WhisperX installation...")
    
    # Try installing a specific compatible version
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "whisperx==3.1.1", "--force-reinstall"
        ], check=True)
        print("✅ WhisperX 3.1.1 installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install WhisperX 3.1.1")
        
    # Try installing the latest version
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "whisperx", "--upgrade"
        ], check=True)
        print("✅ Latest WhisperX installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install latest WhisperX")
        return False

def main():
    """Main function"""
    print("🎤 WhisperX Compatibility Checker")
    print("=" * 40)
    
    # Check if WhisperX is installed
    if not check_whisperx_version():
        print("\n💡 Installing WhisperX...")
        if not fix_whisperx_version():
            print("❌ Could not install WhisperX")
            return 1
    
    # Test API compatibility
    api_version = test_whisperx_api()
    
    if api_version == "new":
        print("\n✅ WhisperX is using the new API - your service should work correctly")
    elif api_version == "old":
        print("\n⚠️ WhisperX is using the old API - updating to handle both versions")
        print("Your service will fall back to the old API automatically")
    else:
        print("\n❌ WhisperX API test failed")
        print("💡 Try running: ./fix_pytorch.sh")
        return 1
    
    print(f"\n🎉 WhisperX compatibility check complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
