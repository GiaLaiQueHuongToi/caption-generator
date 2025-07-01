#!/usr/bin/env python3
"""
Health check script for the Video Caption Generator API.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core imports work correctly"""
    try:
        from src.caption_generator.core.config import settings
        from src.caption_generator.models.video import VideoResponse
        from src.caption_generator.services.video_service import VideoProcessingService
        from src.caption_generator.api.app import app
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from src.caption_generator.core.config import settings
        # Just verify we can access basic settings
        _ = settings.host
        _ = settings.port
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main health check function"""
    print("🏥 Video Caption Generator - Health Check")
    print("=" * 40)
    
    success = True
    
    # Test imports
    if test_imports():
        print("✅ Core imports successful")
    else:
        success = False
    
    # Test configuration
    if test_configuration():
        print("✅ Configuration loaded successfully")
    else:
        success = False
    
    if success:
        print("\n🎉 Health check passed! System is ready.")
    else:
        print("\n❌ Health check failed. Please check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
