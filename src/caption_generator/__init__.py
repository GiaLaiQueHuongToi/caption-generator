"""
Video Caption Generator Package

A FastAPI-based REST API that automatically generates and burns captions 
into videos using WhisperX for transcription and FFmpeg for video processing.
"""

__version__ = "1.0.0"
__author__ = "Video Caption Generator Team"
__description__ = "Automatic video captioning with burned-in subtitles"

from .core.config import settings
from .models.video import VideoResponse
from .services.video_service import VideoProcessingService

__all__ = [
    "settings",
    "VideoResponse",
    "VideoProcessingService",
]
