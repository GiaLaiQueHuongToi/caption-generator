"""
File management utilities for handling uploads, downloads, and temporary files.
"""
import os
import uuid
import tempfile
import shutil
from pathlib import Path
from typing import Optional
import aiofiles
import requests

from ..core.config import settings


class FileManager:
    def __init__(self):
        self.temp_dir = Path(settings.temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        
    def generate_unique_filename(self, extension: str = ".mp4") -> str:
        """Generate a unique filename with UUID"""
        unique_id = str(uuid.uuid4())[:8]
        return f"video_{unique_id}{extension}"
    
    def get_temp_path(self, filename: str) -> Path:
        """Get full path for temporary file"""
        return self.temp_dir / filename
    
    async def save_uploaded_file(self, file_content: bytes, filename: str) -> Path:
        """Save uploaded file to temporary directory"""
        file_path = self.get_temp_path(filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        return file_path
    
    async def download_video_from_url(self, url: str) -> Path:
        """Download video from URL to temporary file"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Try to get extension from URL or Content-Type
        extension = self._get_extension_from_url_or_headers(url, response.headers)
        filename = self.generate_unique_filename(extension)
        file_path = self.get_temp_path(filename)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return file_path
    
    def _get_extension_from_url_or_headers(self, url: str, headers: dict) -> str:
        """Extract file extension from URL or headers"""
        # Try URL first
        url_extension = Path(url.split('?')[0]).suffix
        if url_extension in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            return url_extension
        
        # Try Content-Type header
        content_type = headers.get('content-type', '').lower()
        if 'mp4' in content_type:
            return '.mp4'
        elif 'webm' in content_type:
            return '.webm'
        elif 'quicktime' in content_type:
            return '.mov'
        
        # Default to mp4
        return '.mp4'
    
    def cleanup_file(self, file_path: Path):
        """Remove temporary file"""
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(f"Warning: Could not remove file {file_path}: {e}")
    
    def cleanup_files(self, *file_paths: Path):
        """Remove multiple temporary files"""
        for file_path in file_paths:
            self.cleanup_file(file_path)
