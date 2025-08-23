#!/bin/bash

# Attendance System Setup Script
# This script uses uv to automatically install all required dependencies.

set -e  # Exit on any error

echo "🚀 Attendance System Setup"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root directory."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 uv package manager not found. Installing..."
    pip install uv
    echo "✅ uv installed successfully"
else
    echo "✅ uv package manager is already installed"
fi

# Install Python dependencies using uv
echo ""
echo "🔧 Installing Python dependencies..."
uv sync

# Install face recognition models separately
echo ""
echo "🔧 Installing face recognition models..."
uv pip install git+https://github.com/ageitgey/face_recognition_models || echo "⚠️ Warning: Face recognition models installation failed. You may need to install them manually."

# Create faces directory if it doesn't exist
if [ ! -d "faces" ]; then
    mkdir faces
    echo "✅ Created 'faces' directory for known face images"
else
    echo "✅ 'faces' directory already exists"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add face images to the 'faces/' directory (format: name.jpg)"
echo "2. Run the backend: uv run python main.py"
echo "3. For the frontend, navigate to UI/i-attendance and run: npm install && npm start"
echo ""
echo "💡 To run the application in the future:"
echo "   Backend: uv run python main.py"
echo "   Frontend: cd UI/i-attendance && npm start"