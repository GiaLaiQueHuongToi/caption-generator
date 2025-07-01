"""
FastAPI application for Video Caption Generator API.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from pathlib import Path

from ..models.video import VideoResponse, ErrorResponse
from ..models.subtitle import CaptionPosition
from ..services.video_service import VideoProcessingService
from ..core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Video Caption Generator API",
    description="Automatically generate and burn captions into videos using WhisperX and FFmpeg",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
video_service = VideoProcessingService()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Video Caption Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "generate_captions": "POST /generate-captioned-video",
            "download": "GET /download/{filename}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "video-caption-generator"}

@app.post("/generate-captioned-video", response_model=VideoResponse)
async def generate_captioned_video(
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    font_size: Optional[int] = Form(settings.ffmpeg.default_font_size),
    font_color: Optional[str] = Form(settings.ffmpeg.default_font_color),
    position: Optional[str] = Form(settings.ffmpeg.default_position)
):
    """
    Generate a captioned video with burned-in subtitles.
    
    - **file**: Video file upload (multipart/form-data)
    - **url**: Video URL (alternative to file upload)
    - **font_size**: Caption font size (12-72, default: 24)
    - **font_color**: Caption color (default: white)
    - **position**: Caption position - 'top' or 'bottom' (default: bottom)
    """
    try:
        # Validate input
        if not file and not url:
            raise HTTPException(
                status_code=400,
                detail="Either 'file' or 'url' parameter is required"
            )
        
        if file and url:
            raise HTTPException(
                status_code=400,
                detail="Provide either 'file' or 'url', not both"
            )
        
        # Validate parameters
        if font_size < 12 or font_size > 72:
            raise HTTPException(
                status_code=400,
                detail="Font size must be between 12 and 72"
            )
        
        if position not in ["top", "bottom"]:
            raise HTTPException(
                status_code=400,
                detail="Position must be 'top' or 'bottom'"
            )
        
        # Debug logging to verify parameters
        print(f"🎨 API received styling parameters:")
        print(f"   Font Size: {font_size} (type: {type(font_size)})")
        print(f"   Font Color: '{font_color}' (type: {type(font_color)})")
        print(f"   Position: '{position}' (type: {type(position)})")
        
        # Process video
        result = await video_service.process_video(
            file=file,
            url=url,
            font_size=font_size,
            font_color=font_color,
            position=position
        )
        
        # Schedule cleanup of output file after some time (optional)
        filename = result.video_url.split("/")[-1]
        background_tasks.add_task(
            cleanup_file_after_delay, 
            filename, 
            delay_minutes=30
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/download/{filename}")
async def download_video(filename: str):
    """Download the processed video file"""
    try:
        file_path = video_service.get_download_path(filename)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="video/mp4"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

async def cleanup_file_after_delay(filename: str, delay_minutes: int = 30):
    """Background task to cleanup files after a delay"""
    import asyncio
    await asyncio.sleep(delay_minutes * 60)  # Convert to seconds
    try:
        video_service.cleanup_download_file(filename)
        print(f"Cleaned up file: {filename}")
    except Exception as e:
        print(f"Error cleaning up file {filename}: {e}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=getattr(exc, 'detail', None)
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )

# Create temp directory on startup
@app.on_event("startup")
async def startup_event():
    """Initialize required directories and services"""
    temp_dir = Path(settings.temp_dir)
    temp_dir.mkdir(exist_ok=True)
    print(f"Temp directory created: {temp_dir}")
    
    # Pre-load WhisperX model (optional, will load on first request if this fails)
    try:
        await video_service.whisperx_service.load_model()
        print("WhisperX model loaded successfully")
    except Exception as e:
        print(f"Warning: Could not pre-load WhisperX model: {e}")
        print("Model will be loaded on first transcription request")
