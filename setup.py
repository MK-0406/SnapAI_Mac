from setuptools import setup

APP = ['SnapAI.py']  # Your main script
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'PIL', 'watchdog', 'requests', 'dotenv'],
    'includes': ['pytesseract'],
    'plist': {
        'CFBundleName': 'SnapAI',
        'CFBundleDisplayName': 'SnapAI',
        'CFBundleIdentifier': 'com.snapai.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
