"""
Pydantic models for video processing requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class CaptionPosition(str, Enum):
    """Available caption positions."""
    TOP = "top"
    BOTTOM = "bottom"


class VideoRequest(BaseModel):
    """Request model for video caption generation."""
    
    url: Optional[str] = Field(None, description="Video URL to process")
    font_size: Optional[int] = Field(
        default=24, 
        ge=12, 
        le=72, 
        description="Font size for captions (12-72)"
    )
    font_color: Optional[str] = Field(
        default="white", 
        description="Font color for captions"
    )
    position: Optional[CaptionPosition] = Field(
        default=CaptionPosition.BOTTOM,
        description="Caption position (top or bottom)"
    )
    
    @validator('font_color')
    def validate_font_color(cls, v):
        """Validate font color."""
        if not v or not isinstance(v, str):
            raise ValueError("Font color must be a non-empty string")
        return v.strip().lower()


class VideoResponse(BaseModel):
    """Response model for successful video processing."""
    
    video_url: str = Field(description="URL to download the captioned video")
    message: str = Field(description="Success message")
    processing_time: float = Field(description="Processing time in seconds")
    language_detected: Optional[str] = Field(
        None, 
        description="Detected language code"
    )
    job_id: Optional[str] = Field(None, description="Unique job identifier")


class ErrorResponse(BaseModel):
    """Response model for error cases."""
    
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_code: Optional[str] = Field(None, description="Error code for programmatic handling")


class TranscriptSegment(BaseModel):
    """Model for transcript segments with timing."""
    
    start: float = Field(description="Start time in seconds")
    end: float = Field(description="End time in seconds") 
    text: str = Field(description="Transcript text")
    
    @validator('end')
    def end_after_start(cls, v, values):
        """Ensure end time is after start time."""
        if 'start' in values and v <= values['start']:
            raise ValueError("End time must be after start time")
        return v


class ProcessingStatus(BaseModel):
    """Model for processing status updates."""
    
    job_id: str = Field(description="Unique job identifier")
    status: str = Field(description="Current processing status")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Progress percentage")
    message: Optional[str] = Field(None, description="Status message")
    estimated_time_remaining: Optional[float] = Field(
        None, 
        description="Estimated time remaining in seconds"
    )
