"""
Validation utilities for file size and format checking.
"""
from pathlib import Path

from ..core.config import settings


def validate_file_size(file_content: bytes) -> bool:
    """Validate if file size is within limits"""
    return len(file_content) <= settings.max_file_size


def validate_video_format(filename: str) -> bool:
    """Validate if file has supported video format"""
    supported_formats = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    extension = Path(filename).suffix.lower()
    return extension in supported_formats
