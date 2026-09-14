# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build recipe for MiddleManager.

Build from the repo root:

    pyinstaller MiddleManager.spec

Output is dist/MiddleManager/, roughly 240MB on disk and ~98MB zipped.

onedir rather than onefile on purpose: a onefile exe re-extracts its whole
payload to %TEMP% on every launch, which is a miserable cold start for an app
you leave running in the tray all day.

Two things that look like easy wins and are not:

  - collect_all('mediapipe') is required. MediaPipe ships compiled binaries
    alongside data files (.binarypb graph configs, model bundles) that
    PyInstaller's automatic analysis does not discover. Without it the build
    succeeds and then fails at runtime on a missing resource.

  - matplotlib cannot be excluded, even though nothing here plots anything.
    mediapipe/tasks/python/vision/__init__.py eagerly imports drawing_utils,
    which does `import matplotlib.pyplot` at module level for a 3D plotting
    helper this app never calls. Excluding it builds fine and then crashes on
    startup with ModuleNotFoundError. It costs about 49MB.
"""

import os
import urllib.request

from PyInstaller.utils.hooks import collect_all

MODEL_NAME = "hand_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
             "hand_landmarker/float16/1/hand_landmarker.task")

# The model is gitignored, so a fresh clone will not have it. Fetch it here so
# this spec builds with no prior setup, and bundle it so the packaged app never
# has to download anything on first run.
model_path = os.path.join(SPECPATH, MODEL_NAME)
if not os.path.exists(model_path):
    print(f"[spec] {MODEL_NAME} missing, downloading...")
    urllib.request.urlretrieve(MODEL_URL, model_path)

datas = [(model_path, ".")]
binaries = []
hiddenimports = []

mp_datas, mp_binaries, mp_hiddenimports = collect_all("mediapipe")
datas += mp_datas
binaries += mp_binaries
hiddenimports += mp_hiddenimports

a = Analysis(
    [os.path.join(SPECPATH, "middle_finger_shutdown.py")],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MiddleManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX is off deliberately. It compresses the OpenCV and MediaPipe DLLs,
    # which is a well known source of load failures, and saves little on a
    # payload that is mostly already-compressed model data.
    upx=False,
    console=False,          # tray app: no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="MiddleManager",
)
