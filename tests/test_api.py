import asyncio
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import os

# Add parent directory to path to import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import app
from config import settings

client = TestClient(app)

class TestVideoAPI:
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_missing_input(self):
        """Test API with missing file and URL"""
        response = client.post("/generate-captioned-video")
        assert response.status_code == 400
        assert "Either 'file' or 'url' parameter is required" in response.json()["detail"]
    
    def test_invalid_font_size(self):
        """Test API with invalid font size"""
        response = client.post(
            "/generate-captioned-video",
            data={"url": "https://example.com/video.mp4", "font_size": "100"}
        )
        assert response.status_code == 400
        assert "Font size must be between 12 and 72" in response.json()["detail"]
    
    def test_invalid_position(self):
        """Test API with invalid position"""
        response = client.post(
            "/generate-captioned-video",
            data={"url": "https://example.com/video.mp4", "position": "middle"}
        )
        assert response.status_code == 400
        assert "Position must be 'top' or 'bottom'" in response.json()["detail"]
    
    def test_download_nonexistent_file(self):
        """Test downloading non-existent file"""
        response = client.get("/download/nonexistent.mp4")
        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

# Integration tests would require actual video files and models
# These are placeholder tests for the core API structure

if __name__ == "__main__":
    pytest.main([__file__])
