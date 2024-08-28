import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import tkinter as tk
from tkinter import Label, Button, Text, Scrollbar, VERTICAL, RIGHT, Y, END
from PIL import Image, ImageTk
import threading
import configparser

# Load configuration settings
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    global KNOWN_FACES_DIR, ATTENDANCE_CSV_PATH
    KNOWN_FACES_DIR = config.get('Paths', 'KNOWN_FACES_DIR', fallback='known_faces')
    ATTENDANCE_CSV_PATH = config.get('Paths', 'ATTENDANCE_CSV_PATH', fallback='attendance.csv')

load_config()

# List to store known face encodings and names
known_face_encodings = []
known_face_names = []

# Set to track attendance in the current session
attendance_set = set()

# Load known faces and their encodings
def load_known_faces():
    try:
        for filename in os.listdir(KNOWN_FACES_DIR):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Load an image file
                image_path = os.path.join(KNOWN_FACES_DIR, filename)
                image = face_recognition.load_image_file(image_path)

                # Encode the face
                face_encoding = face_recognition.face_encodings(image)[0]

                # Store the encoding and the name
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])
        update_status("Faces loaded successfully.", "green")
    except Exception as e:
        update_status(f"Error loading faces: {e}", "red")

# Record attendance in a CSV file if not already recorded in the current session
def mark_attendance(name):
    if name not in attendance_set:
        try:
            if not os.path.exists(ATTENDANCE_CSV_PATH):
                with open(ATTENDANCE_CSV_PATH, 'w') as f:
                    f.write('Name,DateTime\n')  # Header for the CSV file

            with open(ATTENDANCE_CSV_PATH, 'a') as f:
                now = datetime.now()
                dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'{name},{dt_string}\n')
            attendance_set.add(name)
            attendance_log.insert(END, f'{name} marked present at {dt_string}\n')
            attendance_log.see(END)
            update_status(f"Attendance marked for {name}.", "green")
        except Exception as e:
            update_status(f"Error marking attendance: {e}", "red")

# Start the camera and process frames
def start_camera(camera_index=0):
    load_known_faces()
    video_capture = cv2.VideoCapture(camera_index)

    while camera_running:
        ret, frame = video_capture.read()
        if not ret:
            update_status("Failed to capture video.", "red")
            break

        rgb_frame = frame[:, :, ::-1]  # Convert the image from BGR to RGB

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the name
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Mark attendance if the face is recognized
            if name != "Unknown":
                mark_attendance(name)

        # Convert the frame to ImageTk format for display in tkinter
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        display_frame.imgtk = imgtk
        display_frame.configure(image=imgtk)

        # Yield to other threads
        root.update()

    video_capture.release()
    cv2.destroyAllWindows()

# Stop the camera
def stop_camera():
    global camera_running
    camera_running = False
    update_status("Camera stopped.", "blue")

# Start a new session
def start_new_session():
    global attendance_set
    attendance_set.clear()
    attendance_log.delete(1.0, END)
    update_status("New session started.", "green")

# Update status in the GUI
def update_status(message, color="black"):
    status_label.config(text=f"Status: {message}", fg=color)

# Authenticate user before starting the application
def authenticate_user():
    password = "admin"
    user_input = input("Enter password: ")
    if user_input != password:
        print("Access denied")
        exit()
    print("Access granted")

# Main function to initialize the GUI
def main():
    authenticate_user()

    global root, display_frame, attendance_log, status_label, camera_running
    root = tk.Tk()
    root.title("Smart Attendance System")

    display_frame = Label(root)
    display_frame.pack()

    start_button = Button(root, text="Start Camera", command=lambda: threading.Thread(target=start_camera_thread).start())
    start_button.pack()

    stop_button = Button(root, text="Stop Camera", command=stop_camera)
    stop_button.pack()

    new_session_button = Button(root, text="New Session", command=start_new_session)
    new_session_button.pack()

    status_label = Label(root, text="Status: Waiting for action", fg="blue")
    status_label.pack()

    scrollbar = Scrollbar(root, orient=VERTICAL)

    attendance_log = Text(root, height=10, yscrollcommand=scrollbar.set)
    attendance_log.pack(side=RIGHT)

    scrollbar.config(command=attendance_log.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    camera_running = False

    root.mainloop()

# Start camera thread
def start_camera_thread():
    global camera_running
    camera_running = True
    start_camera()

if __name__ == "__main__":
    main()
