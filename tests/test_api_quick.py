#!/usr/bin/env python3
"""
Quick API test script
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    """Test API health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_with_sample_url():
    """Test API with a sample video URL"""
    print("\n🧪 Testing with sample video URL...")
    
    # Use a small sample video
    test_url = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
    
    data = {
        'url': test_url,
        'font_size': '24',
        'font_color': 'white',
        'position': 'bottom'
    }
    
    try:
        print("📤 Sending request (this may take a few minutes)...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/generate-captioned-video",
            data=data,
            timeout=300  # 5 minutes timeout
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Processing took {elapsed:.1f} seconds")
            print(f"📹 Video URL: {result.get('video_url', 'N/A')}")
            print(f"🔤 Language detected: {result.get('language_detected', 'N/A')}")
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error: {error_detail}")
            except:
                print(f"Error text: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 API Quick Test")
    print("=" * 30)
    
    # Test health first
    if not test_health():
        print("\n💡 Start the API with: ./start.sh")
        return 1
    
    # Test basic functionality
    if test_with_sample_url():
        print("\n🎉 API is working correctly!")
        return 0
    else:
        print("\n❌ API test failed. Check the server logs for details.")
        print("💡 Common fixes:")
        print("   - Run: python3 check_whisperx.py")
        print("   - Check TROUBLESHOOTING.md")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
