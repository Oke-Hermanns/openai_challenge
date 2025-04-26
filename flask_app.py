import cv2
import mediapipe as mp
import time
from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
from gpt_connection import make_promt
import input_data

app = Flask(__name__)

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Blink detection parameters
blink_threshold = 0.015
blink_duration = 0.5
blink_cooldown = 0.2

last_blink_time = 0
eye_closed = False
blink_start_time = None
blink_detected_flag = False

# Average eye openness from both eyes
def get_avg_eye_openness(landmarks):
    left_eye = abs(landmarks[386].y - landmarks[374].y)
    right_eye = abs(landmarks[159].y - landmarks[145].y)
    return (left_eye + right_eye) / 2

@app.route('/')
def index():
    input_data.user_sentence = ""
    input_data.last_word = ""
    return render_template('index.html')

def gen_frames():
    global last_blink_time, eye_closed, blink_start_time, blink_detected_flag
    cap = cv2.VideoCapture(0) # put camera here
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
                        blink_detected_flag = True
                        last_blink_time = current_time
                    blink_start_time = None
                    eye_closed = False
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/blink')
def check_blink():
    global blink_detected_flag
    blink = blink_detected_flag
    blink_detected_flag = False
    return jsonify({'blink': blink})

def generate_word_suggestions():
    words = make_promt()
    return words

@app.route('/submit', methods=['POST'])
def submit_message():
    message = request.form.get('message', '')
    
    if message:
        input_data.user_sentence = message
        return redirect(url_for('word_selection'))
    else:
        return redirect(url_for('index'))
    
@app.route('/word_selection')
def word_selection():
    words = generate_word_suggestions()
    return render_template('word_selection.html', message=input_data.user_sentence, words=words)

@app.route('/select_word', methods=['POST'])
def select_word():
    user_sentence = input_data.user_sentence
    word = request.form.get('word', '')
    
    if word:
        if user_sentence:
            user_sentence += " " + word
        else:
            user_sentence = word
        input_data.last_word = word
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)