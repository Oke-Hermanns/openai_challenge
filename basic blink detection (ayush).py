import cv2
import mediapipe as mp
import time

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)

# Blink detection parameters
blink_threshold = 0.015  # Adjust this based on print(debug)
blink_duration = 0.5    # Maximum time the eyes can be closed to count as a blink
blink_cooldown = 0.2     # Cooldown time between blinks

last_blink_time = 0
eye_closed = False
blink_start_time = None

# Average eye openness from both eyes
def get_avg_eye_openness(landmarks):
    left_eye = abs(landmarks[386].y - landmarks[374].y)
    right_eye = abs(landmarks[159].y - landmarks[145].y)
    return (left_eye + right_eye) / 2

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

        # Debug: see values
        # print(f"Eye openness: {openness:.4f}")

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

    cv2.imshow("Blink Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
