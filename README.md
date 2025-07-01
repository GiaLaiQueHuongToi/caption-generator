# Video Caption Generator API

A FastAPI-based REST API that automatically generates and burns captions into videos using WhisperX for transcription and FFmpeg for video processing.

## Features

- 🎥 Accepts video files or URLs
- 🗣️ Automatic language detection and transcription
- ⏱️ Word-level timestamp accuracy with WhisperX
- 🎨 Customizable caption styling (font size, color, position)
- 🔥 Burns captions directly into video frames
- 📝 Groups transcription into readable 6-7 word segments
- 🚀 Async processing for concurrent requests
- 🧹 Automatic temporary file cleanup

## Prerequisites

### System Requirements

- Python 3.8+
- FFmpeg installed on system
- CUDA (optional, for GPU acceleration)

### Install FFmpeg

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Installation

1. **Clone and navigate to project:**

```bash
cd caption-generator
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download WhisperX models (first run will auto-download):**

```bash
python -c "import whisperx; whisperx.load_model('large-v2')"
```

## Usage

### Start the API Server

```bash
# Start the server (main entry point)
python main.py

# Or directly with uvicorn
uvicorn src.caption_generator.api.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### API Endpoints

#### Generate Captioned Video

```
POST /generate-captioned-video
```

**Request (multipart/form-data):**

- `file`: Video file (optional if URL provided)
- `url`: Video URL (optional if file provided)
- `font_size`: Caption font size (default: 24)
- `font_color`: Caption color (default: white)
- `position`: Caption position - "top" or "bottom" (default: bottom)

**Response:**

```json
{
  "video_url": "/download/captioned_video_abc123.mp4",
  "message": "Video captioned successfully",
  "processing_time": 45.2
}
```

### Example Client Requests

#### Using curl with file upload:

```bash
curl -X POST "http://localhost:8000/generate-captioned-video" \
  -F "file=@video.mp4" \
  -F "font_size=28" \
  -F "font_color=yellow" \
  -F "position=bottom"
```

#### Using curl with URL:

```bash
curl -X POST "http://localhost:8000/generate-captioned-video" \
  -F "url=https://example.com/video.mp4" \
  -F "font_size=32" \
  -F "font_color=white" \
  -F "position=top"
```

#### Using JavaScript/Axios:

```javascript
const formData = new FormData();
formData.append("file", videoFile);
formData.append("font_size", "28");
formData.append("font_color", "yellow");
formData.append("position", "bottom");

const response = await axios.post(
  "http://localhost:8000/generate-captioned-video",
  formData,
  { headers: { "Content-Type": "multipart/form-data" } }
);

console.log(response.data.video_url);
```

## Configuration

Environment variables (create `.env` file):

```
WHISPERX_MODEL=large-v2
MAX_FILE_SIZE=500000000
TEMP_DIR=./temp
FFMPEG_THREADS=4
```

## Docker Setup (Optional)

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t caption-generator .
docker run -p 8000:8000 caption-generator
```

## Performance Notes

- First request may take longer due to model loading
- GPU acceleration significantly improves processing speed
- Large videos (>100MB) may take several minutes
- Concurrent requests are supported via async processing

## Troubleshooting

**Common Issues:**

1. FFmpeg not found: Ensure FFmpeg is installed and in PATH
2. CUDA errors: Install appropriate PyTorch version for your system
3. Memory issues: Reduce video resolution or use smaller WhisperX model
4. Slow processing: Enable GPU acceleration or use faster model

## API Documentation

Visit `/docs` when server is running for interactive API documentation.
