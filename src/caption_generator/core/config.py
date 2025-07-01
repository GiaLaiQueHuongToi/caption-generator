"""
Core configuration module for the Video Caption Generator.
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AppSettings:
    """Application settings configuration."""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API settings
    API_TITLE: str = "Video Caption Generator API"
    API_DESCRIPTION: str = "Automatically generate and burn captions into videos using WhisperX and FFmpeg"
    API_VERSION: str = "1.0.0"
    
    # File processing settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "500000000"))  # 500MB
    TEMP_DIR: Path = Path(os.getenv("TEMP_DIR", "./temp"))
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"}
    
    # Cleanup settings
    CLEANUP_DELAY_MINUTES: int = int(os.getenv("CLEANUP_DELAY_MINUTES", "30"))


class WhisperXSettings:
    """WhisperX-specific configuration."""
    
    MODEL_NAME: str = os.getenv("WHISPERX_MODEL", "large-v2")
    BATCH_SIZE: int = int(os.getenv("WHISPERX_BATCH_SIZE", "16"))
    
    # Device settings
    FORCE_CPU: bool = os.getenv("CUDA_VISIBLE_DEVICES") == ""
    
    # Caption grouping settings
    WORDS_PER_CAPTION: int = int(os.getenv("WORDS_PER_CAPTION", "7"))
    MIN_WORDS_PER_CAPTION: int = int(os.getenv("MIN_WORDS_PER_CAPTION", "5"))
    MAX_CAPTION_DURATION: float = float(os.getenv("MAX_CAPTION_DURATION", "4.0"))
    MIN_CAPTION_DURATION: float = float(os.getenv("MIN_CAPTION_DURATION", "1.0"))
    
    @property
    def model(self) -> str:
        """Get the model name."""
        return self.MODEL_NAME
    
    @property
    def words_per_caption(self) -> int:
        """Get words per caption."""
        return self.WORDS_PER_CAPTION
    
    @property
    def min_words_per_caption(self) -> int:
        """Get minimum words per caption."""
        return self.MIN_WORDS_PER_CAPTION
    
    @property
    def max_caption_duration(self) -> float:
        """Get maximum caption duration."""
        return self.MAX_CAPTION_DURATION


class FFmpegSettings:
    """FFmpeg-specific configuration."""
    
    THREADS: int = int(os.getenv("FFMPEG_THREADS", "4"))
    PRESET: str = os.getenv("FFMPEG_PRESET", "medium")
    CRF: int = int(os.getenv("FFMPEG_CRF", "23"))
    
    # Default caption styling
    DEFAULT_FONT_SIZE: int = int(os.getenv("DEFAULT_FONT_SIZE", "24"))
    DEFAULT_FONT_COLOR: str = os.getenv("DEFAULT_FONT_COLOR", "white")
    DEFAULT_POSITION: str = os.getenv("DEFAULT_POSITION", "bottom")
    DEFAULT_FONT_NAME: str = os.getenv("DEFAULT_FONT_NAME", "Arial Bold")
    
    # Subtitle styling options
    OUTLINE_SIZE: int = int(os.getenv("OUTLINE_SIZE", "2"))
    SHADOW_SIZE: int = int(os.getenv("SHADOW_SIZE", "1"))
    MARGIN_V: int = int(os.getenv("MARGIN_V", "20"))
    
    @property
    def threads(self) -> int:
        """Get the number of threads."""
        return self.THREADS
    
    @property
    def default_font_size(self) -> int:
        """Get the default font size."""
        return self.DEFAULT_FONT_SIZE
    
    @property
    def default_font_color(self) -> str:
        """Get the default font color."""
        return self.DEFAULT_FONT_COLOR
    
    @property
    def default_position(self) -> str:
        """Get the default position."""
        return self.DEFAULT_POSITION


class Settings:
    """Main settings container."""
    
    def __init__(self):
        self.app = AppSettings()
        self.whisperx = WhisperXSettings()
        self.ffmpeg = FFmpegSettings()
    
    # App properties
    @property
    def host(self) -> str:
        """Get the host."""
        return self.app.HOST
    
    @property
    def port(self) -> int:
        """Get the port."""
        return self.app.PORT
    
    @property
    def max_file_size(self) -> int:
        """Get the maximum file size."""
        return self.app.MAX_FILE_SIZE
        
    @property
    def temp_dir(self) -> Path:
        """Get the temporary directory path."""
        return self.app.TEMP_DIR
    
    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.app.DEBUG
    
    def ensure_temp_dir(self) -> None:
        """Ensure temporary directory exists."""
        self.app.TEMP_DIR.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
