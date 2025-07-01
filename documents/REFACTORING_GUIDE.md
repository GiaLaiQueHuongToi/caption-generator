# Video Caption Generator - Refactored Structure

This document describes the new refactored structure of the Video Caption Generator API.

## 🏗️ Project Structure

```
caption-generator/
├── src/
│   └── caption_generator/              # Main package
│       ├── __init__.py
│       ├── api/                        # FastAPI application
│       │   ├── __init__.py
│       │   └── app.py                  # Main FastAPI app
│       ├── core/                       # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py               # Configuration management
│       │   ├── exceptions.py           # Custom exceptions
│       │   └── logging.py              # Logging configuration
│       ├── models/                     # Pydantic models
│       │   ├── __init__.py
│       │   ├── video.py                # Video-related models
│       │   └── subtitle.py             # Subtitle and transcription models
│       ├── services/                   # Business logic services
│       │   ├── __init__.py
│       │   ├── video_service.py        # Main video processing service
│       │   ├── whisperx_service.py     # WhisperX transcription service
│       │   └── ffmpeg_service.py       # FFmpeg video processing service
│       └── utils/                      # Utility functions
│           ├── __init__.py
│           ├── file_manager.py         # File handling utilities
│           └── validation.py           # Input validation utilities
├── tests/                              # Test files
├── scripts/                            # Utility scripts
├── run_server.py                       # Development server script
├── test_refactor.py                    # Structure validation script
├── main_new.py                         # New main entry point
├── requirements.txt                    # Dependencies
└── README.md                           # Project documentation
```

## 🚀 Running the Application

### Development Mode

```bash
# Using the new development server script
python run_server.py

# Or using the main entry point
python main_new.py

# Or directly with uvicorn
uvicorn src.caption_generator.api.app:app --reload
```

### Production Mode

```bash
uvicorn src.caption_generator.api.app:app --host 0.0.0.0 --port 8000
```

## 📦 Key Components

### Core Module (`src/caption_generator/core/`)

- **config.py**: Centralized configuration management with environment variable support
- **exceptions.py**: Custom exception classes for better error handling
- **logging.py**: Logging configuration and setup

### Models Module (`src/caption_generator/models/`)

- **video.py**: VideoResponse, VideoRequest, and ErrorResponse models
- **subtitle.py**: Transcript segments, caption styling, and SRT-related models

### Services Module (`src/caption_generator/services/`)

- **video_service.py**: Main orchestrator for video processing workflow
- **whisperx_service.py**: WhisperX integration for speech recognition
- **ffmpeg_service.py**: FFmpeg integration for video processing and subtitle burning

### Utils Module (`src/caption_generator/utils/`)

- **file_manager.py**: File upload, download, and temporary file management
- **validation.py**: Input validation functions

### API Module (`src/caption_generator/api/`)

- **app.py**: FastAPI application with all endpoints and middleware

## 🔧 Configuration

The application uses a hierarchical configuration system:

```python
from src.caption_generator.core.config import settings

# Access configuration
print(f"Host: {settings.host}")
print(f"Port: {settings.port}")
print(f"WhisperX model: {settings.whisperx.model}")
print(f"FFmpeg threads: {settings.ffmpeg.threads}")
```

Configuration can be set via environment variables:

```bash
export HOST="0.0.0.0"
export PORT="8000"
export WHISPERX_MODEL="large-v2"
export FFMPEG_THREADS="4"
export DEFAULT_FONT_SIZE="24"
export DEFAULT_FONT_COLOR="white"
```

## 🧪 Testing

### Validate the Refactored Structure

```bash
python test_refactor.py
```

This script tests:

- All imports work correctly
- Configuration loads properly
- Models can be instantiated
- Services can be imported

### Run Existing Tests

The existing test files should still work with the new structure:

```bash
python -m pytest tests/
```

## 📝 Migration from Old Structure

### Import Changes

**Old imports:**

```python
from models import VideoResponse, TranscriptSegment
from video_service import VideoProcessingService
from config import settings
```

**New imports:**

```python
from src.caption_generator.models.video import VideoResponse
from src.caption_generator.models.subtitle import TranscriptSegment
from src.caption_generator.services.video_service import VideoProcessingService
from src.caption_generator.core.config import settings
```

### Entry Point Changes

**Old:**

```bash
python main.py
```

**New:**

```bash
python run_server.py
# or
python main_new.py
```

## 🎯 Benefits of the Refactored Structure

1. **Better Organization**: Clear separation of concerns with dedicated modules
2. **Easier Testing**: Isolated components are easier to unit test
3. **Improved Maintainability**: Changes are localized to specific modules
4. **Better IDE Support**: Proper package structure improves auto-completion and navigation
5. **Scalability**: Easy to add new features without cluttering the root directory
6. **Professional Structure**: Follows Python packaging best practices

## 🔄 Backward Compatibility

The old entry points (`main.py`) are kept for backward compatibility, but using the new structure is recommended for new deployments.
