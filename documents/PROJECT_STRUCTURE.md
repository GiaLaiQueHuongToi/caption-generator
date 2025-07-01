# Video Caption Generator - Project Structure

## 📁 Clean Project Structure

````
caption-generator/
├── src/caption_generator/           # 📦 Main application package
│   ├── api/                        # 🌐 FastAPI application
│   │   ├── __init__.py
│   │   └── app.py                  # Main FastAPI app with routes
│   ├── core/                       # ⚙️ Core functionality
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration management
│   │   ├── exceptions.py           # Custom exceptions
│   │   └── logging.py              # Logging configuration
│   ├── models/                     # � Data models
│   │   ├── __init__.py
│   │   ├── video.py                # Video processing models
│   │   └── subtitle.py             # Subtitle and transcription models
│   ├── services/                   # 🔧 Business logic services
│   │   ├── __init__.py
│   │   ├── video_service.py        # Main video processing orchestrator
│   │   ├── whisperx_service.py     # WhisperX transcription service
│   │   └── ffmpeg_service.py       # FFmpeg video processing service
│   └── utils/                      # 🛠️ Utility functions
│       ├── __init__.py
│       ├── file_manager.py         # File handling utilities
│       └── validation.py           # Input validation utilities
├── tests/                          # 🧪 Test files
├── main.py                         # 🚀 Main entry point
├── health_check.py                 # 🏥 System health check
├── .env.example                    # 📄 Environment variables template
├── requirements.txt                # 📦 Python dependencies
├── Dockerfile                      # 🐳 Docker configuration
├── docker-compose.yml              # 🐳 Docker Compose setup
└── README.md                       # 📚 Project documentation
## � Quick Start

```bash
# 1. Check system health
python health_check.py

# 2. Start the server
python main.py

# 3. Access the API
# http://localhost:8000/docs
````

## 🔧 Key Components

- **main.py**: Primary entry point for starting the server
- **health_check.py**: Quick system validation script
- **src/caption_generator/**: Main application package with modular structure
- **tests/**: Test files for API validation and debugging

## 📚 Documentation

- **README.md**: Complete usage guide and API documentation
- **TROUBLESHOOTING.md**: Common issues and solutions
