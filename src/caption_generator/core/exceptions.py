"""
Custom exception classes for the Video Caption Generator.
"""

from typing import Optional


class CaptionGeneratorError(Exception):
    """Base exception for all caption generator errors."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class VideoProcessingError(CaptionGeneratorError):
    """Raised when video processing fails."""
    pass


class TranscriptionError(CaptionGeneratorError):
    """Raised when audio transcription fails."""
    pass


class FFmpegError(CaptionGeneratorError):
    """Raised when FFmpeg operations fail."""
    pass


class FileValidationError(CaptionGeneratorError):
    """Raised when file validation fails."""
    pass


class ModelLoadError(CaptionGeneratorError):
    """Raised when model loading fails."""
    pass


class SubtitleGenerationError(CaptionGeneratorError):
    """Raised when subtitle generation fails."""
    pass
