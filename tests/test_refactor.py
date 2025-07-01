#!/usr/bin/env python3
"""
Test script to validate the refactored package structure.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all imports work correctly"""
    
    print("Testing imports...")
    
    try:
        # Test core imports
        from src.caption_generator.core.config import settings
        print("✅ Core config import successful")
        
        from src.caption_generator.core.exceptions import CaptionGeneratorError
        print("✅ Core exceptions import successful")
        
        from src.caption_generator.core.logging import setup_logging
        print("✅ Core logging import successful")
        
        # Test model imports
        from src.caption_generator.models.video import VideoResponse, ErrorResponse
        print("✅ Video models import successful")
        
        from src.caption_generator.models.subtitle import (
            TranscriptSegment, CaptionPosition, SubtitleStyle
        )
        print("✅ Subtitle models import successful")
        
        # Test service imports
        from src.caption_generator.services.video_service import VideoProcessingService
        print("✅ Video service import successful")
        
        from src.caption_generator.services.whisperx_service import WhisperXService
        print("✅ WhisperX service import successful")
        
        from src.caption_generator.services.ffmpeg_service import FFmpegService
        print("✅ FFmpeg service import successful")
        
        # Test utils imports
        from src.caption_generator.utils.file_manager import FileManager
        print("✅ File manager import successful")
        
        from src.caption_generator.utils.validation import validate_file_size, validate_video_format
        print("✅ Validation utils import successful")
        
        # Test API imports
        from src.caption_generator.api.app import app
        print("✅ FastAPI app import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from src.caption_generator.core.config import settings
        
        print("\nTesting configuration...")
        print(f"Host: {settings.host}")
        print(f"Port: {settings.port}")
        print(f"Temp dir: {settings.temp_dir}")
        print(f"Max file size: {settings.max_file_size}")
        print(f"WhisperX model: {settings.whisperx.model}")
        print(f"FFmpeg threads: {settings.ffmpeg.threads}")
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_models():
    """Test model creation"""
    try:
        from src.caption_generator.models.video import VideoResponse
        from src.caption_generator.models.subtitle import TranscriptSegment, CaptionPosition
        
        print("\nTesting models...")
        
        # Test video response model
        response = VideoResponse(
            video_url="/download/test.mp4",
            message="Test successful",
            processing_time=1.5,
            language_detected="en"
        )
        print(f"✅ VideoResponse created: {response.video_url}")
        
        # Test transcript segment model
        segment = TranscriptSegment(
            start=0.0,
            end=2.5,
            text="Hello world"
        )
        print(f"✅ TranscriptSegment created: {segment.text}")
        
        # Test caption position enum
        position = CaptionPosition.BOTTOM
        print(f"✅ CaptionPosition enum: {position}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing refactored package structure")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test configuration
    if not test_configuration():
        success = False
    
    # Test models
    if not test_models():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Refactoring successful.")
        print("\nYou can now run the application with:")
        print("python main_new.py")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
