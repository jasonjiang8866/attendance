import cv2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from face_recognizor import FaceRecognition

app = FastAPI()
app.fr = FaceRecognition()
templates = Jinja2Templates(directory="templates")

def gen_frames():
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
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)