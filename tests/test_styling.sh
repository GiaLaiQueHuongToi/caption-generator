#!/bin/bash

# Test script to verify subtitle styling options

echo "🎨 Testing Video Caption Styling Options"
echo "========================================"

API_URL="http://localhost:8000"

# Check if API is running
echo "🔍 Checking API status..."
if ! curl -s "$API_URL/health" > /dev/null; then
    echo "❌ API is not running. Start it with: ./start.sh"
    exit 1
fi
echo "✅ API is running"

# Sample video URL (replace with your own for testing)
VIDEO_URL="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"

echo ""
echo "📝 Testing different styling combinations..."
echo "   Using video URL: $VIDEO_URL"
echo ""

# Test 1: Large Yellow Bottom
echo "1️⃣ Testing: Large Yellow Bottom (36px)"
curl -X POST "$API_URL/generate-captioned-video" \
  -F "url=$VIDEO_URL" \
  -F "font_size=36" \
  -F "font_color=yellow" \
  -F "position=bottom" \
  --progress-bar | jq '.video_url, .message, .processing_time'

echo ""

# Test 2: Small White Top
echo "2️⃣ Testing: Small White Top (16px)"
curl -X POST "$API_URL/generate-captioned-video" \
  -F "url=$VIDEO_URL" \
  -F "font_size=16" \
  -F "font_color=white" \
  -F "position=top" \
  --progress-bar | jq '.video_url, .message, .processing_time'

echo ""

# Test 3: Medium Red Bottom
echo "3️⃣ Testing: Medium Red Bottom (28px)"
curl -X POST "$API_URL/generate-captioned-video" \
  -F "url=$VIDEO_URL" \
  -F "font_size=28" \
  -F "font_color=red" \
  -F "position=bottom" \
  --progress-bar | jq '.video_url, .message, .processing_time'

echo ""

# Test 4: Large Blue Top
echo "4️⃣ Testing: Large Blue Top (48px)"
curl -X POST "$API_URL/generate-captioned-video" \
  -F "url=$VIDEO_URL" \
  -F "font_size=48" \
  -F "font_color=blue" \
  -F "position=top" \
  --progress-bar | jq '.video_url, .message, .processing_time'

echo ""
echo "🎉 Styling tests complete!"
echo ""
echo "💡 Tips:"
echo "   - Download the videos to check if styling is applied correctly"
echo "   - Bottom position should show captions at the bottom of the video"
echo "   - Top position should show captions at the top of the video"
echo "   - Font sizes should be visibly different"
echo "   - Colors should be clearly visible"
