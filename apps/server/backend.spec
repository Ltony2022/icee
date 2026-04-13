# -*- mode: python ; coding: utf-8 -*-

from __future__ import annotations

import sys
import os
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

# We assume the build script runs this spec with CWD set to apps/server
BASE_DIR = Path(os.getcwd()).resolve()
ROOT_DIR = BASE_DIR.parent.parent

distpath = str(BASE_DIR / "dist")
workpath = str(BASE_DIR / "build")

# Ensure local packages (backend, blocker, etc.) are importable while this spec runs.
for path in (ROOT_DIR, BASE_DIR, ROOT_DIR / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

block_cipher = None
hiddenimports = []

# Third-party deps that need to be force-included when PyInstaller misses them.
hiddenimports += collect_submodules("waitress")

for package in ("backend", "blocker", "flashcard", "pomodoro", "helpers", "application_blocker"):
    hiddenimports += collect_submodules(package)
hiddenimports += collect_submodules("dns_proxy")
hiddenimports += ["pyuac", "wmi", "pythoncom", "icoextract", "PIL", "win32com"]

datas = [
    (str((BASE_DIR / "db.sqlite3")), "."),
    (str((ROOT_DIR / "proxy" / "dns_proxy.py")), "proxy"),
    (str((ROOT_DIR / "proxy" / "blocked_domains.txt")), "proxy"),
]

a = Analysis(
    ["run_backend.py"],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="backend-service",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="backend-service",
)

