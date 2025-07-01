#!/usr/bin/env python3
"""
Main entry point for the Video Caption Generator API.
"""

import uvicorn
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.caption_generator.core.config import settings

def main():
    """Run the Video Caption Generator API server."""
    print("🚀 Starting Video Caption Generator API")
    print(f"   Host: {settings.host}:{settings.port}")
    print(f"   Debug: {settings.is_debug}")
    print(f"   Temp dir: {settings.temp_dir}")
    
    # Ensure temp directory exists
    settings.ensure_temp_dir()
    
    uvicorn.run(
        "src.caption_generator.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()
