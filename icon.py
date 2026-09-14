"""MiddleManager's artwork, in one place.

Both the tray icon and the .ico bundled into the exe and the installer come from
here, so they cannot drift apart. Regenerate the .ico with:

    python icon.py

The build does this for you -- MiddleManager.spec calls write_ico() -- which is
why the .ico is gitignored rather than committed.
"""

from PIL import Image, ImageDraw

# Drawn on a 64x64 grid and scaled from there, because that is the size the tray
# actually renders at.
BASE = 64

BACKGROUND   = "#1a1a1a"
FINGER       = "#ffffff"
FINGER_ARMED = "#ff4444"
KNUCKLES     = "#555555"
FIST         = "#ffffff"

ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

def create_icon(armed=False, size=BASE):
    img = Image.new("RGB", (size, size), color=BACKGROUND)
    draw = ImageDraw.Draw(img)
    scale = size / BASE

    def box(x0, y0, x1, y1):
        return [x0 * scale, y0 * scale, x1 * scale, y1 * scale]

    draw.rectangle(box(26, 10, 38, 45), fill=FINGER_ARMED if armed else FINGER)
    draw.rectangle(box(14, 28, 25, 45), fill=KNUCKLES)
    draw.rectangle(box(39, 28, 50, 45), fill=KNUCKLES)
    draw.rectangle(box(20, 45, 44, 54), fill=FIST)
    return img

def write_ico(path):
    """Write a multi-resolution .ico for the exe, shortcuts and installer."""
    largest = max(ICO_SIZES)[0]
    create_icon(size=largest).save(path, format="ICO", sizes=ICO_SIZES)
    return path

if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MiddleManager.ico")
    print("wrote", write_ico(out))
