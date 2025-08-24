import cv2
import uvicorn
import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from face_recognizor import FaceRecognition

app = FastAPI()

# Add CORS middleware to allow requests from Angular app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.fr = FaceRecognition()
templates = Jinja2Templates(directory="templates")

# Initialize attendance log file
ATTENDANCE_LOG_FILE = "attendance_log.json"

def load_attendance_log():
    """Load attendance records from file"""
    if os.path.exists(ATTENDANCE_LOG_FILE):
        with open(ATTENDANCE_LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_attendance_log(records):
    """Save attendance records to file"""
    with open(ATTENDANCE_LOG_FILE, 'w') as f:
        json.dump(records, f, indent=2)

def record_attendance(name):
    """Record attendance for a recognized person"""
    records = load_attendance_log()
    timestamp = datetime.now().isoformat()
    
    # Check if person already marked attendance today
    today = datetime.now().date().isoformat()
    today_records = [r for r in records if r['name'] == name and r['timestamp'].startswith(today)]
    
    if not today_records:
        new_record = {
            "name": name,
            "timestamp": timestamp,
            "date": today
        }
        records.append(new_record)
        save_attendance_log(records)
        return True
    return False

def gen_frames(flag):
    try:
        app.camera.release()
    except Exception as e:
        print(e)
    app.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        success, frame = app.camera.read()
        if not success:
            break
        else:
            frame = app.fr.process_frame(frame)
            app.fr.process_current_frame = not app.fr.process_current_frame               
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed')
def video_feed(request: Request):
    flag = request.query_params.get('flag')
    return StreamingResponse(gen_frames(flag), media_type='multipart/x-mixed-replace; boundary=frame')

@app.post('/register_face')
async def register_face(name: str = Form(...), image: UploadFile = File(...)):
    """Register a new face with the given name"""
    try:
        # Ensure faces directory exists
        if not os.path.exists('faces'):
            os.makedirs('faces')
        
        # Save uploaded image
        image_path = f"faces/{name}.jpg"
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # Re-encode faces to include the new face
        app.fr.encode_faces()
        
        return JSONResponse({
            "success": True,
            "message": f"Face registered successfully for {name}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/mark_attendance')
async def mark_attendance(name: str = Form(...)):
    """Mark attendance for a recognized person"""
    try:
        success = record_attendance(name)
        if success:
            return JSONResponse({
                "success": True,
                "message": f"Attendance marked for {name}"
            })
        else:
            return JSONResponse({
                "success": False,
                "message": f"Attendance already marked for {name} today"
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/attendance_records')
def get_attendance_records():
    """Get all attendance records"""
    try:
        records = load_attendance_log()
        return JSONResponse({"records": records})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/registered_faces')
def get_registered_faces():
    """Get list of registered faces"""
    try:
        faces = []
        if os.path.exists('faces'):
            faces = [f.split('.')[0] for f in os.listdir('faces') if f.endswith(('.jpg', '.jpeg', '.png'))]
        return JSONResponse({"faces": faces})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)