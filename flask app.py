import cv2
import mediapipe as mp
import time
from flask import Flask, render_template, Response

# Initialize Flask
app = Flask(__name__)

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)

# Blink detection parameters
blink_threshold = 0.015
blink_duration = 0.5
blink_cooldown = 0.2

last_blink_time = 0
eye_closed = False
blink_start_time = None

# Average eye openness from both eyes
def get_avg_eye_openness(landmarks):
    left_eye = abs(landmarks[386].y - landmarks[374].y)
    right_eye = abs(landmarks[159].y - landmarks[145].y)
    return (left_eye + right_eye) / 2

# Route to serve the HTML page with the grid and message box
@app.route('/')
def index():
    return render_template('index.html')

# Function to generate webcam feed for Flask
def gen_frames():
    global last_blink_time, eye_closed, blink_start_time
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            openness = get_avg_eye_openness(landmarks)

            current_time = time.time()

            if openness < blink_threshold:
                if not eye_closed:
                    blink_start_time = current_time
                    eye_closed = True
            else:
                if eye_closed and blink_start_time:
                    blink_time = current_time - blink_start_time
                    if blink_time < blink_duration and current_time - last_blink_time > blink_cooldown:
                        print("Blink detected!")
                        last_blink_time = current_time
                    blink_start_time = None
                    eye_closed = False

        # Convert frame to JPEG format for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route to stream webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
