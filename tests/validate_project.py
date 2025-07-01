#!/usr/bin/env python3
"""
Project validation script for Video Caption Generator
Checks if all required files and dependencies are properly configured
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_python_import(module_name):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ Python module: {module_name}")
        return True
    except ImportError:
        print(f"❌ Python module: {module_name} - NOT INSTALLED")
        return False

def check_system_command(command):
    """Check if a system command is available"""
    try:
        subprocess.run([command, "--version"], 
                      capture_output=True, check=True)
        print(f"✅ System command: {command}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ System command: {command} - NOT FOUND")
        return False

def main():
    """Main validation function"""
    print("🔍 Video Caption Generator - Project Validation")
    print("=" * 50)
    
    all_good = True
    
    # Check core Python files
    print("\n📄 Core Files:")
    core_files = [
        ("main.py", "FastAPI main application"),
        ("config.py", "Configuration file"),
        ("models.py", "Pydantic models"),
        ("utils.py", "Utility functions"),
        ("whisperx_service.py", "WhisperX service"),
        ("ffmpeg_service.py", "FFmpeg service"),
        ("video_service.py", "Video processing service"),
        ("requirements.txt", "Python dependencies"),
    ]
    
    for filepath, description in core_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check setup files
    print("\n🔧 Setup Files:")
    setup_files = [
        ("setup.sh", "Setup script"),
        ("start.sh", "Start script"),
        ("README.md", "Documentation"),
        (".env.example", "Environment template"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose"),
    ]
    
    for filepath, description in setup_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check system dependencies
    print("\n🖥️ System Dependencies:")
    system_deps = ["python3", "ffmpeg"]
    
    for command in system_deps:
        if not check_system_command(command):
            all_good = False
    
    # Check if virtual environment exists
    print("\n🐍 Python Environment:")
    if Path("venv").exists():
        print("✅ Virtual environment: venv/")
        
        # Try to check installed packages if venv is activated
        if os.getenv("VIRTUAL_ENV"):
            print("✅ Virtual environment is activated")
            
            # Check key Python dependencies
            print("\n📦 Python Dependencies:")
            key_modules = [
                "fastapi",
                "uvicorn",
                "whisperx", 
                "torch",
                "requests",
                "aiofiles",
                "pydantic"
            ]
            
            for module in key_modules:
                if not check_python_import(module):
                    all_good = False
        else:
            print("⚠️ Virtual environment exists but not activated")
            print("💡 Run: source venv/bin/activate")
    else:
        print("❌ Virtual environment: venv/ - NOT FOUND")
        print("💡 Run: ./setup.sh")
        all_good = False
    
    # Check temp directory
    print("\n📁 Directories:")
    if Path("temp").exists():
        print("✅ Temp directory: temp/")
    else:
        print("⚠️ Temp directory: temp/ - will be created on startup")
    
    # Final status
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Project validation PASSED!")
        print("🚀 Ready to start the API server with: ./start.sh")
    else:
        print("❌ Project validation FAILED!")
        print("🔧 Please fix the issues above before starting")
        print("💡 Run ./setup.sh to install dependencies")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
