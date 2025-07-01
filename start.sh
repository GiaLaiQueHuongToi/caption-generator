#!/bin/bash

# Quick start script for Video Caption Generator

echo "🚀 Starting Video Caption Generator API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
fi

# Create temp directory if it doesn't exist
mkdir -p temp

# Start the API server
echo "🌟 Starting FastAPI server..."
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo "🔗 Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
