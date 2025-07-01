#!/usr/bin/env python3
"""
Direct FFmpeg subtitle testing script
"""

import subprocess
import tempfile
from pathlib import Path

def create_test_srt():
    """Create a simple test SRT file"""
    srt_content = """1
00:00:01,000 --> 00:00:03,000
This is a test caption

2
00:00:04,000 --> 00:00:06,000
Testing font styling options

3
00:00:07,000 --> 00:00:09,000
Yellow large text at bottom

4
00:00:10,000 --> 00:00:12,000
Different colors and sizes
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        f.write(srt_content)
        return Path(f.name)

def test_ffmpeg_styling():
    """Test FFmpeg subtitle styling directly"""
    print("🧪 Testing FFmpeg subtitle styling directly...")
    
    # Create test SRT
    srt_path = create_test_srt()
    print(f"Created test SRT: {srt_path}")
    
    # Test different styling options
    test_cases = [
        {
            "name": "Large Yellow Bottom",
            "font_size": 36,
            "color": "yellow", 
            "position": "bottom",
            "alignment": "2"
        },
        {
            "name": "Small Red Top",
            "font_size": 16,
            "color": "red",
            "position": "top", 
            "alignment": "8"
        }
    ]
    
    for test in test_cases:
        print(f"\n📝 Testing: {test['name']}")
        
        # Color conversion (BGR format for ASS)
        color_map = {
            "yellow": "00FFFF",
            "red": "0000FF",
            "white": "FFFFFF",
            "blue": "FF0000"
        }
        
        color_hex = color_map.get(test['color'], "FFFFFF")
        
        force_style = (
            f"FontName=Arial Bold,"
            f"FontSize={test['font_size']},"
            f"PrimaryColour=&H{color_hex},"
            f"OutlineColour=&H000000,"
            f"BackColour=&H80000000,"
            f"Outline=2,"
            f"Shadow=1,"
            f"Alignment={test['alignment']},"
            f"MarginV=20"
        )
        
        print(f"   Force style: {force_style}")
        
        # Test command (without actual video input)
        cmd = [
            "ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=15:size=1280x720:rate=30",
            "-vf", f"subtitles={srt_path}:force_style='{force_style}'",
            "-t", "15", "-y", f"test_{test['color']}_{test['position']}.mp4"
        ]
        
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"   ✅ Success! Created test_{test['color']}_{test['position']}.mp4")
            else:
                print(f"   ❌ Failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Cleanup
    srt_path.unlink()
    print(f"\nCleaned up test SRT file")

if __name__ == "__main__":
    test_ffmpeg_styling()
