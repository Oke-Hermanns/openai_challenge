import cv2
import mediapipe as mp
import time
import tkinter as tk

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

# Create Tkinter window
root = tk.Tk()
root.title("Blink-to-Text")

# Create message box
message_box = tk.Entry(root, font=("Arial", 16), width=40)
message_box.pack(pady=10)

# Create grid for letters
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
grid_frame = tk.Frame(root)
grid_frame.pack()

# Create a 3x9 grid of labels (A-Z) for letters
labels = {}
row_highlight = 0  # Initially highlight the first row
letter_highlight = 0  # Initially highlight the first letter
is_row_locked = False
is_letter_locked = False
message = []

for i in range(3):
    row = tk.Frame(grid_frame)
    row.pack()
    for j in range(9):
        letter = alphabet[i * 9 + j] if i * 9 + j < len(alphabet) else ""
        label = tk.Label(row, text=letter, font=("Arial", 14), width=4, height=2, borderwidth=2, relief="solid")
        label.grid(row=0, column=j)
        labels[letter] = label

# Function to update the grid highlight
def update_highlight():
    for letter, label in labels.items():
        label.config(bg="white")  # Reset all highlights

    # Highlight the row
    row_start = row_highlight * 9
    for i in range(9):
        letter = alphabet[row_start + i] if row_start + i < len(alphabet) else ""
        labels[letter].config(bg="lightblue")

    # Highlight the letter in the row
    if not is_row_locked:
        letter = alphabet[row_highlight * 9 + letter_highlight]
        labels[letter].config(bg="lightgreen")

# Update the message box
def update_message():
    message_box.delete(0, tk.END)
    message_box.insert(0, ''.join(message))

# Blink detection and row/letter handling
def process_blink():
    global last_blink_time, eye_closed, blink_start_time, row_highlight, letter_highlight, is_row_locked, is_letter_locked

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        openness = get_avg_eye_openness(landmarks)

        current_time = time.time()

        # Blink detection logic
        if openness < blink_threshold:
            if not eye_closed:
                blink_start_time = current_time
                eye_closed = True
        else:
            if eye_closed and blink_start_time:
                blink_time = current_time - blink_start_time
                if blink_time < blink_duration and current_time - last_blink_time > blink_cooldown:
                    if not is_row_locked:
                        print(f"Row {row_highlight + 1} locked!")
                        is_row_locked = True
                    elif not is_letter_locked:
                        letter = alphabet[row_highlight * 9 + letter_highlight]
                        print(f"Letter {letter} selected!")
                        message.append(letter)
                        update_message()
                        is_letter_locked = True
                        row_highlight = (row_highlight + 1) % 3  # Move to next row

                    last_blink_time = current_time
                blink_start_time = None
                eye_closed = False

    # Update the grid highlight and check letter selection
    update_highlight()

# Function to cycle through the letters in the row every second
def cycle_letters():
    global letter_highlight, is_row_locked, is_letter_locked
    if not is_row_locked:
        letter_highlight = (letter_highlight + 1) % 9
    else:
        if is_letter_locked:
            is_row_locked = False
            is_letter_locked = False
        else:
            letter_highlight = (letter_highlight + 1) % 9
    root.after(1000, cycle_letters)  # Continue cycling every second

# Start the letter cycling
cycle_letters()

# Main loop to process OpenCV and Tkinter updates
while True:
    process_blink()
    root.update_idletasks()
    root.update()

    # Close the window on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
root.quit()
