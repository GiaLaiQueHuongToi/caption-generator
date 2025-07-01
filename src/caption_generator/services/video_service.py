"""
Video processing service for handling video transcription and captioning.
"""
import time
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

from .whisperx_service import WhisperXService
from .ffmpeg_service import FFmpegService
from ..utils.file_manager import FileManager
from ..utils.validation import validate_file_size, validate_video_format
from ..models.video import VideoResponse
from ..models.subtitle import TranscriptSegment
from ..core.config import settings


class VideoProcessingService:
    def __init__(self):
        self.whisperx_service = WhisperXService()
        self.ffmpeg_service = FFmpegService()
        self.file_manager = FileManager()
    
    async def process_video(
        self,
        file: Optional[UploadFile] = None,
        url: Optional[str] = None,
        font_size: int = settings.ffmpeg.default_font_size,
        font_color: str = settings.ffmpeg.default_font_color,
        position: str = settings.ffmpeg.default_position
    ) -> VideoResponse:
        """Process video to add captions"""
        start_time = time.time()
        
        # Temporary file paths
        input_video_path = None
        srt_path = None
        output_video_path = None
        
        try:
            # Step 1: Get input video
            if file:
                input_video_path = await self._handle_uploaded_file(file)
            elif url:
                input_video_path = await self._handle_video_url(url)
            else:
                raise ValueError("Either file or URL must be provided")
            
            # Step 2: Transcribe video with WhisperX
            print("Starting transcription...")
            transcription_result = await self.whisperx_service.transcribe_video(input_video_path)
            
            # Step 3: Group words into caption segments
            print("Grouping words into captions...")
            captions = self.whisperx_service.group_words_into_captions(
                transcription_result["segments"]
            )
            
            if not captions:
                raise ValueError("No speech detected in video")
            
            # Step 4: Create SRT file
            print("Creating SRT file...")
            srt_content = self.whisperx_service.create_srt_content(captions)
            srt_path = self.file_manager.get_temp_path(
                f"subtitles_{self.file_manager.generate_unique_filename('.srt')}"
            )
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            # Step 5: Burn subtitles into video
            print("Burning subtitles into video...")
            output_filename = f"captioned_{self.file_manager.generate_unique_filename()}"
            output_video_path = self.file_manager.get_temp_path(output_filename)
            
            await self.ffmpeg_service.burn_subtitles(
                video_path=input_video_path,
                srt_path=srt_path,
                output_path=output_video_path,
                font_size=font_size,
                font_color=font_color,
                position=position
            )
            
            processing_time = time.time() - start_time
            
            # Return response with download URL
            download_url = f"/download/{output_filename}"
            
            return VideoResponse(
                video_url=download_url,
                message="Video captioned successfully",
                processing_time=round(processing_time, 2),
                language_detected=transcription_result["language"]
            )
            
        except Exception as e:
            # Cleanup on error
            if input_video_path and file:  # Only cleanup uploaded files
                self.file_manager.cleanup_file(input_video_path)
            if srt_path:
                self.file_manager.cleanup_file(srt_path)
            if output_video_path:
                self.file_manager.cleanup_file(output_video_path)
            raise e
        
        finally:
            # Cleanup input files (but keep output for download)
            if input_video_path and file:  # Only cleanup uploaded files
                self.file_manager.cleanup_file(input_video_path)
            if srt_path:
                self.file_manager.cleanup_file(srt_path)
    
    async def _handle_uploaded_file(self, file: UploadFile) -> Path:
        """Handle uploaded video file"""
        # Validate file format
        if not validate_video_format(file.filename):
            raise ValueError(f"Unsupported video format: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        if not validate_file_size(file_content):
            raise ValueError(f"File too large. Maximum size: {settings.max_file_size} bytes")
        
        # Save to temporary file
        temp_filename = self.file_manager.generate_unique_filename(
            Path(file.filename).suffix
        )
        return await self.file_manager.save_uploaded_file(file_content, temp_filename)
    
    async def _handle_video_url(self, url: str) -> Path:
        """Handle video URL download"""
        return await self.file_manager.download_video_from_url(url)
    
    def get_download_path(self, filename: str) -> Path:
        """Get path for download file"""
        return self.file_manager.get_temp_path(filename)
    
    def cleanup_download_file(self, filename: str):
        """Cleanup downloaded file after serving"""
        file_path = self.get_download_path(filename)
        self.file_manager.cleanup_file(file_path)
