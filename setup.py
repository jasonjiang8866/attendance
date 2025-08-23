#!/usr/bin/env python3
"""
Setup script for the Attendance System with Face Recognition
This script uses uv to automatically install all required dependencies.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_uv_installed():
    """Check if uv is installed."""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_uv():
    """Install uv if not already installed."""
    print("\n📦 Installing uv package manager...")
    if not run_command("pip install uv", "Installing uv via pip"):
        print("❌ Failed to install uv. Please install it manually:")
        print("   pip install uv")
        return False
    return True

def main():
    print("🚀 Attendance System Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("❌ Error: pyproject.toml not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if uv is installed
    if not check_uv_installed():
        print("📦 uv package manager not found. Installing...")
        if not install_uv():
            sys.exit(1)
    else:
        print("✅ uv package manager is already installed")
    
    # Install Python dependencies using uv
    if not run_command("uv sync", "Installing Python dependencies"):
        print("\n❌ Failed to install Python dependencies")
        print("You can try installing manually with:")
        print("   uv sync")
        sys.exit(1)
    
    # Install face recognition models separately due to face_recognition package requirements
    print("\n🔧 Installing face recognition models...")
    if not run_command("uv pip install git+https://github.com/ageitgey/face_recognition_models", "Installing face recognition models"):
        print("⚠️ Warning: Face recognition models installation failed")
        print("You may need to install them manually with:")
        print("   uv pip install git+https://github.com/ageitgey/face_recognition_models")
    
    # Create faces directory if it doesn't exist
    faces_dir = "faces"
    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)
        print(f"✅ Created '{faces_dir}' directory for known face images")
    else:
        print(f"✅ '{faces_dir}' directory already exists")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add face images to the 'faces/' directory (format: name.jpg)")
    print("2. Run the backend: uv run python main.py")
    print("3. For the frontend, navigate to UI/i-attendance and run: npm install && npm start")
    print("\n💡 To run the application in the future:")
    print("   Backend: uv run python main.py")
    print("   Frontend: cd UI/i-attendance && npm start")

if __name__ == "__main__":
    main()