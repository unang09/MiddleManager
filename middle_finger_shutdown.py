import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import subprocess
import tkinter as tk
import threading
import time
import sys
import urllib.request
import os

# --- Download model if needed ---

MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("[INFO] Downloading hand landmarker model (~9MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("[INFO] Model downloaded.")

# --- Gesture Detection ---

def is_finger_extended(landmarks, tip_id, pip_id):
    return landmarks[tip_id].y < landmarks[pip_id].y

def is_middle_finger_up(landmarks):
    middle_up  = is_finger_extended(landmarks, 12, 10)
    index_down = not is_finger_extended(landmarks, 8, 6)
    ring_down  = not is_finger_extended(landmarks, 16, 14)
    pinky_down = not is_finger_extended(landmarks, 20, 18)
    return middle_up and index_down and ring_down and pinky_down

base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# --- Countdown Window ---

class CountdownWindow:
    def __init__(self, on_cancel):
        self.on_cancel = on_cancel
        self.root = tk.Tk()
        self.root.title("Shutdown Triggered")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

        w, h = 380, 180
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 22, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        self.label.pack(pady=(28, 8))

        self.sub = tk.Label(
            self.root,
            text="Shutting down...",
            font=("Segoe UI", 11),
            fg="#aaaaaa",
            bg="#1a1a1a"
        )
        self.sub.pack()

        self.cancel_btn = tk.Button(
            self.root,
            text="Cancel  (press any key or click)",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#c0392b",
            activebackground="#e74c3c",
            activeforeground="#ffffff",
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.cancel
        )
        self.cancel_btn.pack(pady=(14, 0))

        self.root.bind("<Key>", lambda e: self.cancel())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.cancelled = False

    def update_label(self, n):
        self.label.config(text=f"Shutting down in {n}...")

    def cancel(self):
        self.cancelled = True
        self.root.destroy()
        self.on_cancel()

    def run(self):
        self.root.mainloop()

# --- Main App ---

class MiddleFingerApp:
    def __init__(self):
        self.countdown_active = False

    def on_cancel(self):
        self.countdown_active = False
        print("[INFO] Shutdown cancelled.")

    def trigger_shutdown(self):
        self.countdown_active = True
        win = CountdownWindow(on_cancel=self.on_cancel)

        def countdown():
            for i in range(5, 0, -1):
                if win.cancelled:
                    return
                win.root.after(0, win.update_label, i)
                time.sleep(1)
            if not win.cancelled:
                win.root.after(0, win.root.destroy)
                print("[ACTION] Shutting down NOW.")
                subprocess.run(["shutdown", "/s", "/t", "0"])

        threading.Thread(target=countdown, daemon=True).start()
        win.run()

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[ERROR] Cannot open webcam.")
            sys.exit(1)

        print("[INFO] MiddleManager is watching... Show it who's boss.")
        print("[INFO] Press Q in the webcam window to quit.")

        gesture_hold_frames = 0
        required_frames = 10

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(mp_image)

            detected = False
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    if is_middle_finger_up(hand_landmarks):
                        detected = True

            if detected and not self.countdown_active:
                gesture_hold_frames += 1
                cv2.putText(frame, f"DETECTED ({gesture_hold_frames}/{required_frames})",
                            (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if gesture_hold_frames >= required_frames:
                    gesture_hold_frames = 0
                    print("[INFO] Middle finger detected! Triggering shutdown countdown.")
                    threading.Thread(target=self.trigger_shutdown, daemon=True).start()
            else:
                gesture_hold_frames = max(0, gesture_hold_frames - 1)

            cv2.putText(frame, "MiddleManager", (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.imshow("MiddleManager", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        detector.close()
        print("[INFO] MiddleManager closed.")

if __name__ == "__main__":
    app = MiddleFingerApp()
    app.run()