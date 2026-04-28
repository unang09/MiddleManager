# MiddleManager 🖕

![Made with Rage](https://img.shields.io/badge/made%20with-rage-cc0000?style=flat-square&labelColor=1a1a1a)
![Works on My Machine](https://img.shields.io/badge/works%20on-my%20machine-6a0dad?style=flat-square&labelColor=1a1a1a)
![Windows](https://img.shields.io/badge/platform-windows-0078d4?style=flat-square&labelColor=1a1a1a)
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-f7c948?style=flat-square&labelColor=1a1a1a)
![License MIT](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square&labelColor=1a1a1a)

> Shut down your laptop the way it deserves.

MiddleManager is a Windows desktop app that watches your webcam, detects when you flip it off, and shuts your computer down. No buttons. No menus. Just you, your finger, and zero regrets.

---

## Why

Every day, millions of people endure frozen screens, surprise updates, and soul-crushing load times — and are expected to just click **Shut Down** like a civilised person.

Nobody feels good about that. Nobody.

MiddleManager fixes this.

---

## Demo

1. Open MiddleManager
2. Flip off your webcam
3. Watch the 5-second countdown
4. Cancel if you've had a change of heart _(you won't)_
5. Your laptop shuts down

---

## Installation

**Requirements**

- Windows 10 / 11
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
middlemanager-env\Scriptsctivate
```

**Install dependencies**

```bash
pip install opencv-python mediapipe
```

**Run**

```bash
python middle_finger_shutdown.py
```

On first run, the app will automatically download the MediaPipe hand landmarker model (~9MB). After that it works offline.

---

## How it works

MiddleManager uses [MediaPipe](https://developers.google.com/mediapipe) to detect hand landmarks in real time via your webcam. It checks whether:

- The middle finger is extended
- All other fingers (index, ring, pinky) are curled

The gesture must be held for ~10 consecutive frames to trigger — so a passing wave won't accidentally nuke your unsaved work.

Once confirmed, a countdown window appears. You have 5 seconds to cancel by clicking the button, pressing any key, or closing the window. If you don't, `shutdown /s /t 0` runs and Windows goes down.

Press **Q** in the webcam window to quit the app entirely.

---

## Sensitivity / false triggers

The gesture requires all four conditions to be met simultaneously — middle finger up, and index, ring, and pinky all curled. It's specific enough that accidental triggers are rare, but if you work in an environment where spontaneous middle fingers are common, that's a you problem.

---

## Contributing

PRs welcome. Ideas that would make this better:

- System tray icon so it runs silently in the background
- Custom sound on trigger
- Support for other gestures (thumbs down → sleep, double finger guns → restart)

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
A: We cannot stop you. We would not stop you. We are, in fact, proud of you.

**Q: My laptop didn't shut down. Why?**
A: Windows probably started an update mid-shutdown. There is nothing we can do. There is nothing anyone can do.

**Q: Is there a Pro version?**
A: The Pro version is the same app but you paid for it. Coming never.

**Q: What is the meaning of life?**
A: Flip off your laptop and find out.

---

This app will shut down your computer. Unsaved work will be lost. The developer is not responsible for lost documents, failed deadlines, or strained relationships with your laptop. Use responsibly — or don't, that's kind of the point.

---

## License

MIT. Do whatever you want with it. Your computer, your finger, your call.

---

_\* 73% of workers have rage-stared at their laptop this week. Statistic completely made up. The feeling is real._
