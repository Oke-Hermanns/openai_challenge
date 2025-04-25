import cv2
import mediapipe as mp
import time

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)

blink_threshold = 0.02  # adjust based on camera
blink_cooldown = 1.0  # seconds
last_blink_time = 0

def get_eye_openness(landmarks, top_idx, bottom_idx):
    return abs(landmarks[top_idx].y - landmarks[bottom_idx].y)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Blink detection from left eye
        openness = get_eye_openness(landmarks, 386, 374)

        if openness < blink_threshold and time.time() - last_blink_time > blink_cooldown:
            print("Blink detected!")
            last_blink_time = time.time()

    cv2.imshow("Blink Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
