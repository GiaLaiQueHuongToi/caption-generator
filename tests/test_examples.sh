#!/bin/bash

# Video Caption Generator API - Test Examples

API_URL="http://localhost:8000"

echo "🎥 Video Caption Generator API - Test Examples"
echo "=============================================="

# Function to check API status
check_api() {
    echo "🔍 Checking API status..."
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
    if [ "$response" = "200" ]; then
        echo "✅ API is running"
        return 0
    else
        echo "❌ API is not responding (HTTP $response)"
        echo "💡 Start the API with: ./start.sh"
        return 1
    fi
}

# Test with file upload
test_file_upload() {
    echo ""
    echo "📁 Testing file upload..."
    echo "📝 Please provide a video file path:"
    read -r video_file
    
    if [ ! -f "$video_file" ]; then
        echo "❌ File not found: $video_file"
        return 1
    fi
    
    echo "🎬 Uploading video: $video_file"
    echo "⏳ This may take several minutes..."
    
    curl -X POST "$API_URL/generate-captioned-video" \
        -F "file=@$video_file" \
        -F "font_size=28" \
        -F "font_color=yellow" \
        -F "position=bottom" \
        --progress-bar
}

# Test with URL
test_url() {
    echo ""
    echo "🌐 Testing with video URL..."
    echo "📝 Enter video URL (or press Enter for sample):"
    read -r video_url
    
    if [ -z "$video_url" ]; then
        video_url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
        echo "Using sample URL: $video_url"
    fi
    
    echo "🎬 Processing video from URL..."
    echo "⏳ This may take several minutes..."
    
    curl -X POST "$API_URL/generate-captioned-video" \
        -F "url=$video_url" \
        -F "font_size=32" \
        -F "font_color=white" \
        -F "position=top" \
        --progress-bar
}

# Test API endpoints
test_endpoints() {
    echo ""
    echo "🧪 Testing API endpoints..."
    
    echo "📋 Root endpoint:"
    curl -s "$API_URL/" | python3 -m json.tool
    
    echo ""
    echo "💚 Health check:"
    curl -s "$API_URL/health" | python3 -m json.tool
}

# Download video example
download_example() {
    echo ""
    echo "📥 Download example:"
    echo "curl -O \"$API_URL/download/captioned_video_abc123.mp4\""
}

# Main menu
main_menu() {
    while true; do
        echo ""
        echo "🎯 Choose an option:"
        echo "1. Check API status"
        echo "2. Test file upload"
        echo "3. Test URL processing"
        echo "4. Test API endpoints"
        echo "5. Show download example"
        echo "6. Exit"
        echo ""
        read -p "Enter choice (1-6): " choice
        
        case $choice in
            1)
                check_api
                ;;
            2)
                if check_api; then
                    test_file_upload
                fi
                ;;
            3)
                if check_api; then
                    test_url
                fi
                ;;
            4)
                if check_api; then
                    test_endpoints
                fi
                ;;
            5)
                download_example
                ;;
            6)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice"
                ;;
        esac
    done
}

# Run main menu
main_menu
