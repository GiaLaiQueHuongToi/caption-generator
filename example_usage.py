#!/usr/bin/env python3
"""
Example usage script for the Video Caption Generator API
"""

import requests
import json
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/generate-captioned-video"

def test_with_file_upload():
    """Test API with file upload"""
    print("🎬 Testing with file upload...")
    
    # Example video file path (replace with your video)
    video_file = "sample_video.mp4"
    
    if not Path(video_file).exists():
        print(f"❌ Video file not found: {video_file}")
        print("Please provide a valid video file for testing")
        return
    
    # Prepare request data
    files = {
        'file': ('video.mp4', open(video_file, 'rb'), 'video/mp4')
    }
    
    data = {
        'font_size': '28',
        'font_color': 'yellow',
        'position': 'bottom'
    }
    
    try:
        print("📤 Uploading video and generating captions...")
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"📹 Video URL: {result['video_url']}")
            print(f"🔤 Language detected: {result['language_detected']}")
            print(f"⏱️ Processing time: {result['processing_time']} seconds")
            
            # Download the result
            download_video(result['video_url'])
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out. Video processing may take several minutes.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        files['file'][1].close()

def test_with_url():
    """Test API with video URL"""
    print("🌐 Testing with video URL...")
    
    # Example video URL (replace with actual URL)
    video_url = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
    
    data = {
        'url': video_url,
        'font_size': '32',
        'font_color': 'white',
        'position': 'top'
    }
    
    try:
        print("📥 Processing video from URL...")
        response = requests.post(UPLOAD_ENDPOINT, data=data, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"📹 Video URL: {result['video_url']}")
            print(f"🔤 Language detected: {result['language_detected']}")
            print(f"⏱️ Processing time: {result['processing_time']} seconds")
            
            # Download the result
            download_video(result['video_url'])
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out. Video processing may take several minutes.")
    except Exception as e:
        print(f"❌ Error: {e}")

def download_video(video_path):
    """Download the processed video"""
    download_url = f"{API_BASE_URL}{video_path}"
    print(f"📥 Downloading video from: {download_url}")
    
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            filename = video_path.split('/')[-1]
            output_path = f"output_{filename}"
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Video saved as: {output_path}")
        else:
            print(f"❌ Download failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Download error: {e}")

def check_api_status():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Error checking API: {e}")
        return False

def main():
    """Main function to run examples"""
    print("🎥 Video Caption Generator API - Example Usage")
    print("=" * 50)
    
    # Check API status
    if not check_api_status():
        print("\n💡 To start the API server:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("\n🧪 Choose test method:")
    print("1. File upload test")
    print("2. URL test")
    print("3. Both tests")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_with_file_upload()
    elif choice == "2":
        test_with_url()
    elif choice == "3":
        test_with_file_upload()
        print("\n" + "="*50)
        test_with_url()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
