# Attendance System with Face Recognition

A real-time attendance tracking system that uses facial recognition technology to automatically identify and record attendance. The system consists of a Python FastAPI backend with face recognition capabilities and an Angular frontend for user interaction.

## 🚀 Features

- **Real-time Face Recognition**: Uses OpenCV and face_recognition library for accurate face detection and identification
- **Live Video Streaming**: Real-time webcam feed with face detection overlay
- **Web-based Interface**: Modern Angular frontend with Material Design components
- **RESTful API**: FastAPI backend for handling video streams and face recognition processing
- **Automatic Attendance**: Seamless attendance tracking through facial recognition
- **Known Face Management**: System to encode and store known faces for recognition

## 📸 User Interface Screenshots

### Face Registration
The system provides an intuitive interface for registering new faces. Users can upload a clear photo along with their name to register for attendance tracking.

![Face Registration Interface](screenshots/face-registration-tab.png)

### Live Attendance Tracking
The main attendance interface features a live video feed with real-time face recognition capabilities, plus manual attendance options as a fallback.

![Take Attendance Interface](screenshots/take-attendance-tab.png)

### Attendance Records
View and manage attendance history with a clean, organized interface showing timestamps and recent attendance activities.

![Attendance Records Interface](screenshots/attendance-records-tab.png)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **OpenCV**: Computer vision library for image processing
- **face_recognition**: Face recognition library built on dlib
- **Uvicorn**: ASGI server for running the FastAPI application

### Frontend
- **Angular 16**: Modern web application framework
- **Angular Material**: Material Design components for Angular
- **Bootstrap**: CSS framework for responsive design
- **TypeScript**: Typed superset of JavaScript

## 📋 Prerequisites

### Python Dependencies
- Python 3.7+
- OpenCV (`cv2`)
- face_recognition
- FastAPI
- Uvicorn
- NumPy

### Node.js Dependencies
- Node.js 16+
- Angular CLI
- npm or yarn

## 🔧 Installation

### Option 1: Automatic Setup (Recommended)

We provide automated setup scripts that use [uv](https://github.com/astral-sh/uv) for fast and reliable Python dependency management:

```bash
# Clone the repository
git clone https://github.com/jasonjiang8866/attendance.git
cd attendance

# Run the automated setup script (Python)
python setup.py

# Or use the shell script alternative
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Install uv package manager if not already installed
- Create a virtual environment and install all Python dependencies
- Install face recognition models
- Create the required 'faces' directory

### Option 2: Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/jasonjiang8866/attendance.git
cd attendance
```

#### 2. Backend Setup
```bash
# Install Python dependencies manually
pip install fastapi uvicorn opencv-python face-recognition numpy jinja2

# Create a 'faces' directory and add known face images
mkdir faces
# Add images of known people to the faces directory (format: name.jpg)
```

#### 3. Frontend Setup
```bash
# Navigate to the Angular application
cd UI/i-attendance

# Install dependencies
npm install

# Build the application
npm run build
```

## 🚀 Usage

### Running the Backend

If you used the automated setup (recommended):
```bash
# From the repository root
uv run python main.py
```

If you used manual installation:
```bash
# From the repository root
python main.py
```

The FastAPI server will start on `http://127.0.0.1:8000`

### Running the Frontend
```bash
# Navigate to the Angular application
cd UI/i-attendance

# Start the development server
npm start
```
The Angular application will be available on `http://localhost:4200`

### API Endpoints
- `GET /`: Main interface with live video stream
- `GET /video_feed`: Video streaming endpoint for face recognition

## 📁 Project Structure

```
attendance/
├── README.md                 # This file
├── main.py                   # FastAPI backend application
├── face_recognizor.py        # Face recognition logic and processing
├── setup.py                  # Automated Python setup script for developers
├── setup.sh                  # Automated shell setup script for developers
├── pyproject.toml           # Python project configuration and dependencies
├── .python-version          # Python version specification for uv
├── templates/                # HTML templates for the web interface
│   └── index.html           # Main template for video streaming
├── UI/                      # Frontend application
│   └── i-attendance/        # Angular application
│       ├── src/             # Angular source code
│       ├── package.json     # Node.js dependencies
│       └── README.md        # Angular-specific README
├── faces/                   # Directory for known face images (created by setup)
├── .gitignore              # Git ignore rules
└── known_face_*.dat        # Generated face encoding files
```

## 🎯 How It Works

1. **Face Encoding**: The system scans the `faces/` directory and creates encodings for all known faces
2. **Real-time Detection**: Uses webcam feed to detect faces in real-time
3. **Recognition**: Compares detected faces with known face encodings
4. **Confidence Scoring**: Provides confidence percentage for face matches
5. **Visual Feedback**: Displays bounding boxes and names on the video feed

## 📝 Adding New Faces

1. Add high-quality images of people to the `faces/` directory
2. Name the files with the person's name (e.g., `john_doe.jpg`)
3. Restart the application to update the face encodings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Important Notes

- Ensure good lighting conditions for optimal face recognition accuracy
- The system requires camera permissions to function properly
- Face recognition accuracy depends on the quality of images in the `faces/` directory
- For production use, consider implementing additional security measures and data protection

## 🔧 Troubleshooting

### Common Issues
- **Camera not detected**: Ensure your webcam is connected and not being used by other applications
- **Face recognition not working**: Check if the `faces/` directory contains images and face encodings are generated
- **Performance issues**: Reduce video frame size or adjust processing frequency in the code

### Requirements Installation Issues
If you encounter issues installing face_recognition:
```bash
# On Ubuntu/Debian
sudo apt-get install cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev

# On macOS
brew install cmake
```

## 📞 Support

For support and questions, please open an issue in the GitHub repository.