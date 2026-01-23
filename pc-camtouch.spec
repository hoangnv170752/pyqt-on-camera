# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for PC CamTouch Windows build
Run: pyinstaller pc-camtouch.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Collect all source files
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pygame',
        'pygame.mixer',
        'cv2',
        'numpy',
        'loguru',
        'psutil',
        'pyvidplayer2',
        'src.app',
        'src.widgets.video_widget',
        'src.widgets.grid_view',
        'src.widgets.home_screen',
        'src.widgets.camera_dialog',
        'src.widgets.status_indicators',
        'src.services.database',
        'src.services.logger',
        'src.services.resource_monitor',
        'src.services.stream_manager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'test',
        'unittest',
        'email',
        'http',
        'xml',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PC CamTouch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one: 'icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PC CamTouch',
)
