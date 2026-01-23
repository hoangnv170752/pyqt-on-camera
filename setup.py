"""
Setup script for building macOS application bundle using py2app
Run: python setup.py py2app
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'PyQt6',
        'pyvidplayer2',
        'cv2',
        'loguru',
        'psutil',
    ],
    'includes': [
        'src',
        'src.app',
        'src.widgets',
        'src.services',
        'pygame',
    ],
    'excludes': ['tkinter', 'matplotlib', 'numpy.distutils', 'test'],
    'resources': [],
    'plist': {
        'CFBundleName': 'PC CamTouch',
        'CFBundleDisplayName': 'PC CamTouch',
        'CFBundleIdentifier': 'com.camtouch.pccamtouch',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
}

setup(
    name='PC CamTouch',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)
