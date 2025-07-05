"""
Models for subtitle and transcription data.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import timedelta
from enum import Enum


class CaptionPosition(str, Enum):
    """Enum for caption position."""
    TOP = "top"
    BOTTOM = "bottom"


class WordAlignment(BaseModel):
    """Model for word-level alignment data."""
    
    word: str = Field(description="The word text")
    start: float = Field(description="Start time in seconds")
    end: float = Field(description="End time in seconds")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")


class TranscriptSegment(BaseModel):
    """Model for simple transcript segments for captioning."""
    
    start: float = Field(description="Start time in seconds")
    end: float = Field(description="End time in seconds")
    text: str = Field(description="Segment text")
    
    @validator('end')
    def end_after_start(cls, v, values):
        """Ensure end time is after start time."""
        if 'start' in values and v <= values['start']:
            raise ValueError("End time must be after start time")
        return v


class TranscriptionSegment(BaseModel):
    """Model for transcription segments."""
    
    id: int = Field(description="Segment ID")
    start: float = Field(description="Start time in seconds")
    end: float = Field(description="End time in seconds")
    text: str = Field(description="Segment text")
    words: Optional[List[WordAlignment]] = Field(None, description="Word-level alignments")
    language: Optional[str] = Field(None, description="Detected language")
    
    @validator('end')
    def end_after_start(cls, v, values):
        """Ensure end time is after start time."""
        if 'start' in values and v <= values['start']:
            raise ValueError("End time must be after start time")
        return v


class TranscriptionResult(BaseModel):
    """Model for complete transcription results."""
    
    language: str = Field(description="Detected language code")
    segments: List[TranscriptionSegment] = Field(description="Transcription segments")
    duration: float = Field(description="Total audio duration in seconds")
    model_used: str = Field(description="WhisperX model used")
    processing_time: float = Field(description="Processing time in seconds")


class SubtitleStyle(BaseModel):
    """Model for subtitle styling options."""
    
    font_size: int = Field(24, ge=12, le=72, description="Font size")
    font_color: str = Field("white", description="Font color")
    font_name: str = Field("Arial Bold", description="Font name")
    position: str = Field("bottom", description="Position (top/bottom)")
    outline_size: int = Field(2, ge=0, le=10, description="Outline thickness")
    shadow_size: int = Field(1, ge=0, le=10, description="Shadow size")
    margin_v: int = Field(20, ge=0, le=100, description="Vertical margin")
    
    @validator('font_color')
    def validate_color(cls, v):
        """Validate font color format."""
        if not v or not isinstance(v, str):
            raise ValueError("Font color must be a non-empty string")
        return v.strip().lower()


class SRTEntry(BaseModel):
    """Model for SRT subtitle entries."""
    
    index: int = Field(description="Subtitle index")
    start_time: str = Field(description="Start time in SRT format")
    end_time: str = Field(description="End time in SRT format")
    text: str = Field(description="Subtitle text")
    
    def to_srt_block(self) -> str:
        """Convert to SRT format block."""
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.text}\n"
