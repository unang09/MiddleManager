# MiddleManager 🖕

![Made with Rage](https://img.shields.io/badge/made%20with-rage-cc0000?style=flat-square&labelColor=1a1a1a)
![Works on My Machine](https://img.shields.io/badge/works%20on-my%20machine-6a0dad?style=flat-square&labelColor=1a1a1a)
![Windows](https://img.shields.io/badge/platform-windows-0078d4?style=flat-square&labelColor=1a1a1a)
![Linux](https://img.shields.io/badge/platform-linux-E95420?style=flat-square&labelColor=1a1a1a)
![Python 3.12](https://img.shields.io/badge/python-3.12-f7c948?style=flat-square&labelColor=1a1a1a)
![License MIT](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square&labelColor=1a1a1a)

> Shut down your laptop the way it deserves.

MiddleManager is a Windows and Linux desktop app that sits silently in your system tray, watches your webcam on demand, and shuts your computer down when you flip it off. No buttons. No menus. Just you, your finger, and zero regrets.

---

## Why

Every day, millions of people endure frozen screens, surprise updates, and soul-crushing load times — and are expected to just click **Shut Down** like a civilised person.

Nobody feels good about that. Nobody.

MiddleManager fixes this.

---

## Demo

1. Run MiddleManager — it hides silently in your system tray
2. Press `Ctrl+Alt+M` to wake the camera for 10 seconds
3. Flip off your webcam
4. Watch the 5-second countdown
5. Cancel if you've had a change of heart _(you won't)_
6. Your laptop shuts down

---

## Features

- **Runs in the background** — lives in the system tray, no visible window
- **On-demand camera** — camera only activates when you press the hotkey, not 24/7
- **Global hotkey** — `Ctrl+Alt+M` wakes the camera from anywhere, no matter what app is focused
- **Two modes** — Manual (hotkey works anytime) or Schedule (hotkey only works Mon–Fri, 9am–5pm)
- **5-second countdown** — with a cancel button, for the weak of heart
- **Cross-platform** — works on Windows and Linux

---

## Installation

**Requirements**

- Windows 10 / 11 or Linux
- Python 3.12 (specifically — MediaPipe does not support 3.13 or 3.14, because Google hates you)
- A webcam
- Pent-up frustration

**Get Python 3.12.10**

Download the Windows 64-bit installer from the [official release page](https://www.python.org/downloads/release/python-31210/). During installation, check **"Add Python to PATH"**.

**Clone the repo**

```bash
git clone git@github.com:yourusername/MiddleManager.git
cd MiddleManager
```

**Create a virtual environment**

```bash
py -3.12 -m venv middlemanager-env
middlemanager-env\Scripts\activate
```

**Install dependencies**

```bash
pip install opencv-python mediapipe pystray pillow pynput
```

**Run**

```bash
python middle_finger_shutdown.py
```

On first run, the app will automatically download the MediaPipe hand landmarker model (~9MB). After that it works offline.

---

## How it works

MiddleManager runs silently in the system tray and does nothing until you need it.

Press `Ctrl+Alt+M` — the camera activates for 10 seconds. During that window, MediaPipe reads each frame and checks whether:

- The middle finger is extended
- All other fingers (index, ring, pinky) are curled

The gesture must be held for ~10 consecutive frames to trigger — so a passing wave won't accidentally nuke your unsaved work. If no gesture is detected within 10 seconds, the camera shuts off and goes back to sleep.

Once triggered, a countdown window appears center-screen. You have 5 seconds to cancel by clicking the button, pressing any key, or closing the window. If you don't — it's over.

---

## Modes

Right-click the tray icon to switch between modes.

**Manual** — the hotkey works anytime, any day. Maximum chaos.

**Schedule** — the hotkey only works Monday to Friday, 9am to 5pm. Outside those hours, pressing `Ctrl+Alt+M` does nothing. For when you want MiddleManager to understand work-life balance better than your employer does.

---

## Sensitivity / false triggers

The gesture requires all four conditions to be met simultaneously — middle finger up, and index, ring, and pinky all curled. It's specific enough that accidental triggers are rare, but if you work in an environment where spontaneous middle fingers are common, that's a you problem.

---

## Contributing

PRs welcome. Ideas that would make this better:

- Custom sound on trigger
- Support for other gestures (thumbs down → sleep, double finger guns → restart)
- Configurable work hours for Schedule mode
- Configurable hotkey

---

## FAQ

**Q: Is this safe to use?**
A: Absolutely. It will only shut down your computer. It will not, to our knowledge, shut down your marriage, career, or sense of self-worth. Those were already gone before you installed this.

**Q: What if I accidentally trigger it?**
A: You have 5 seconds. That is 5 full seconds. If you cannot cancel a shutdown in 5 seconds, MiddleManager is the least of your problems.

**Q: Will it work on my left hand?**
A: Yes. We do not discriminate. MiddleManager respects all fingers equally, as long as it's the middle one.

**Q: What if my laptop crashes before I can flip it off?**
A: Then your laptop has already defeated you. Seek help.

**Q: Does this work on Mac?**
A: No. Mac users have therapy and aesthetic consistency. They do not need this.

**Q: Can I set it to restart instead of shutdown?**
A: No. There is no restart. There is no coming back. You made your choice.

**Q: What if my coworker sees me flipping off my webcam?**
A: Tell them it's a "proprietary gesture-based productivity interface." Do not elaborate.

**Q: Does it work in the dark?**
A: Depends on your webcam. If it can't see your finger, that's between you and your hardware manufacturer.

**Q: I showed it to my boss and got fired. Can I sue you?**
A: The license is MIT. You accepted all responsibility the moment you ran `python middle_finger_shutdown.py`. We wish you well.

**Q: Can I use this at work?**
A: We cannot stop you. We would not stop you. We are, in fact, proud of you. Consider using Schedule mode for maximum professionalism.

**Q: Why does the hotkey only work during work hours in Schedule mode?**
A: Because your laptop also deserves to clock out. Unlike you.

**Q: I'm on Linux and it doesn't shut down. Why?**
A: `shutdown -h now` requires sudo privileges on Linux. Run the app with `sudo python middle_finger_shutdown.py`, or add a sudoers rule so it can run without a password:

```
echo "$USER ALL=(ALL) NOPASSWD: /sbin/shutdown" | sudo tee /etc/sudoers.d/middlemanager
```

Yes, you are granting a finger-detection app the right to shut down your computer. You knew what you signed up for.

**Q: My laptop didn't shut down. Why?**
A: Windows probably started an update mid-shutdown. There is nothing we can do. There is nothing anyone can do.

**Q: Is there a Pro version?**
A: The Pro version is the same app but you paid for it. Coming never.

**Q: What is the meaning of life?**
A: Flip off your laptop and find out.

---

## Disclaimer

This app will shut down your computer. Unsaved work will be lost. The developer is not responsible for lost documents, failed deadlines, or strained relationships with your laptop. Use responsibly — or don't, that's kind of the point.

---

## License

MIT. Do whatever you want with it. Your computer, your finger, your call.

---

_\* 73% of workers have rage-stared at their laptop this week. Statistic completely made up. The feeling is real._
