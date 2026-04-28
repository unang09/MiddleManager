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
import platform
import os
from PIL import Image, ImageDraw
import pystray
from pynput import keyboard

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

# --- Tray Icon ---

def create_icon(armed=False):
    img = Image.new("RGB", (64, 64), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    finger_color = "#ff4444" if armed else "#ffffff"
    draw.rectangle([26, 10, 38, 45], fill=finger_color)
    draw.rectangle([14, 28, 25, 45], fill="#555555")
    draw.rectangle([39, 28, 50, 45], fill="#555555")
    draw.rectangle([20, 45, 44, 54], fill="#ffffff")
    return img

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

        self.label = tk.Label(self.root, text="",
            font=("Segoe UI", 22, "bold"), fg="#ffffff", bg="#1a1a1a")
        self.label.pack(pady=(28, 8))

        tk.Label(self.root, text="Shutting down...",
            font=("Segoe UI", 11), fg="#aaaaaa", bg="#1a1a1a").pack()

        tk.Button(self.root, text="Cancel  (press any key or click)",
            font=("Segoe UI", 10), fg="#ffffff", bg="#c0392b",
            activebackground="#e74c3c", activeforeground="#ffffff",
            relief="flat", padx=16, pady=8, cursor="hand2",
            command=self.cancel).pack(pady=(14, 0))

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

MODE_MANUAL   = "manual"
MODE_SCHEDULE = "schedule"

SCHEDULE_DAYS  = {0, 1, 2, 3, 4}  # Mon–Fri
SCHEDULE_START = 9   # 9am
SCHEDULE_END   = 17  # 5pm

class MiddleFingerApp:
    def __init__(self):
        self.countdown_active = False
        self.listening = False
        self.running = True
        self.mode = MODE_MANUAL
        self.tray = None
        self.hotkey_listener = None

    def in_schedule_window(self):
        now = time.localtime()
        return (now.tm_wday in SCHEDULE_DAYS and
                SCHEDULE_START <= now.tm_hour < SCHEDULE_END)

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
                if platform.system() == "Windows":
                    subprocess.run(["shutdown", "/s", "/t", "0"])
                elif platform.system() == "Linux":
                    subprocess.run(["shutdown", "-h", "now"])
                else:
                    print("[ERROR] Unsupported OS.")

        threading.Thread(target=countdown, daemon=True).start()
        win.run()

    def activate_camera(self):
        """Wake camera for 10 seconds and watch for gesture."""
        if self.listening or self.countdown_active:
            return

        # In schedule mode, only allow during work hours
        if self.mode == MODE_SCHEDULE and not self.in_schedule_window():
            print("[INFO] Outside work hours. Hotkey ignored.")
            self.update_tray_status()
            return

        print("[INFO] Camera activated — watching for 10 seconds.")
        self.listening = True
        self.update_tray_status()

        def camera_session():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("[ERROR] Cannot open webcam.")
                self.listening = False
                self.update_tray_status()
                return

            gesture_hold_frames = 0
            required_frames = 10
            end_time = time.time() + 10

            while time.time() < end_time and self.listening:
                ret, frame = cap.read()
                if not ret:
                    continue

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
                    if gesture_hold_frames >= required_frames:
                        cap.release()
                        self.listening = False
                        print("[INFO] Middle finger detected! Triggering shutdown.")
                        self.update_tray_status()
                        threading.Thread(target=self.trigger_shutdown, daemon=True).start()
                        return
                else:
                    gesture_hold_frames = max(0, gesture_hold_frames - 1)

            cap.release()
            self.listening = False
            print("[INFO] Camera session ended — no gesture detected.")
            self.update_tray_status()

        threading.Thread(target=camera_session, daemon=True).start()

    def on_hotkey(self):
        threading.Thread(target=self.activate_camera, daemon=True).start()

    def start_hotkey_listener(self):
        def on_activate():
            print("[INFO] Hotkey triggered!")
            self.on_hotkey()

        self.hotkey_listener = keyboard.GlobalHotKeys({
            "<ctrl>+<alt>+m": on_activate
        })
        self.hotkey_listener.start()

    def get_status_text(self):
        if self.countdown_active:
            return "Status: Shutting down..."
        if self.listening:
            return "Status: Listening \U0001f440"
        if self.mode == MODE_SCHEDULE:
            if self.in_schedule_window():
                return "Status: Scheduled — ready"
            return "Status: Scheduled — off hours"
        return "Status: Sleeping"

    def update_tray_status(self):
        if self.tray:
            self.tray.icon = create_icon(armed=self.listening)
            self.tray.menu = self.build_menu()

    def set_mode_manual(self, icon, item):
        self.mode = MODE_MANUAL
        print("[INFO] Mode: Manual")
        self.update_tray_status()

    def set_mode_schedule(self, icon, item):
        self.mode = MODE_SCHEDULE
        print("[INFO] Mode: Schedule (Mon–Fri, 9am–5pm)")
        self.update_tray_status()

    def quit_app(self, icon, item):
        print("[INFO] Quitting MiddleManager.")
        self.running = False
        self.listening = False
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        icon.stop()
        detector.close()
        os._exit(0)

    def build_menu(self):
        return pystray.Menu(
            pystray.MenuItem(self.get_status_text(), None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Hotkey: Ctrl+Alt+M", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Mode", pystray.Menu(
                pystray.MenuItem(
                    "Manual",
                    self.set_mode_manual,
                    checked=lambda item: self.mode == MODE_MANUAL,
                    radio=True
                ),
                pystray.MenuItem(
                    "Schedule (Mon–Fri, 9am–5pm)",
                    self.set_mode_schedule,
                    checked=lambda item: self.mode == MODE_SCHEDULE,
                    radio=True
                ),
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )

    def run(self):
        self.start_hotkey_listener()

        icon_image = create_icon(armed=False)
        self.tray = pystray.Icon(
            "MiddleManager",
            icon_image,
            "MiddleManager \U0001f595",
            self.build_menu()
        )
        print("[INFO] MiddleManager running. Press Ctrl+Alt+M to activate.")
        self.tray.run()

if __name__ == "__main__":
    app = MiddleFingerApp()
    app.run()