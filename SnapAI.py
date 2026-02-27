import sys
import os

log_file = os.path.expanduser("~/snapai_log.txt")
sys.stdout = open(log_file, "a")
sys.stderr = sys.stdout
print("\n\n--- SnapAI launched ---\n")

import time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
from PIL import Image
import requests
from PyQt5 import QtWidgets, QtCore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

AI_MODEL = "gemini-2.5-flash"
model = genai.GenerativeModel(AI_MODEL)
WATCHED_FOLDER = os.path.expanduser("~/Downloads")

class FloatingPanel(QtWidgets.QWidget):
    updateTextSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.94)

        self.setStyleSheet("""
            QWidget {
                border-radius: 14px;
                background-color: rgba(20, 20, 20, 180);
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border-radius: 10px;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(200, 200, 200, 0.6);
                border-radius: 4px;
            }
        """)

        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)

        self.label = QtWidgets.QTextEdit()
        self.label.setReadOnly(True)
        self.label.setMarkdown("Welcome to SnapAI...")
        self.label.setStyleSheet("""
            QTextEdit {
                color: white;
                font-size: 16px;
                background: transparent;
                border: none;
            }
        """)
        self.label.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)

        self.content_layout.addWidget(self.label)
        self.scroll.setWidget(self.content_widget)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton("Start")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.quit_btn = QtWidgets.QPushButton("Quit")

        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.quit_btn.clicked.connect(QtWidgets.qApp.quit)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.quit_btn)
        layout.addLayout(button_layout)

        self.setFixedSize(460, 260)
        self.move(400, 200)
        self.show()

        self.observer = None
        self.handler = None
        self.monitoring = False
        self.updateTextSignal.connect(self.update_text)
        QtCore.QTimer.singleShot(0, lambda: force_mac_floating_window(self))

    @QtCore.pyqtSlot(str)
    def update_text(self, new_text):
        self.label.setMarkdown(new_text)

    def start_monitoring(self):
        if self.monitoring:
            return
        self.handler = ScreenshotHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.handler, WATCHED_FOLDER, recursive=False)
        self.observer.start()
        self.update_text("Monitoring started...")
        self.monitoring = True

    def stop_monitoring(self):
        if self.observer and self.monitoring:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.update_text("Monitoring stopped.")
            self.monitoring = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, panel):
        self.panel = panel

    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return
        self.panel.updateTextSignal.emit("Processing screenshot...")
        Thread(target=self.process_screenshot, args=(event.src_path,), daemon=True).start()

    def process_screenshot(self, path):
        time.sleep(1)
        try:
            text = pytesseract.image_to_string(Image.open(path))
            text = "Please give a short answer\n" + text
            print("🖼️ OCR Text:", text)
            if text.strip():
                self.panel.updateTextSignal.emit("Asking AI...")
                ai_response = ask_ai(text)
                self.panel.updateTextSignal.emit(ai_response)
        except Exception as e:
            print("Error:", e)

def force_mac_floating_window(widget):
    try:
        from AppKit import NSApp, NSFloatingWindowLevel, NSWindowCollectionBehaviorCanJoinAllSpaces, NSWindowCollectionBehaviorFullScreenAuxiliary
        ns_window = NSApp().windows()[-1]
        ns_window.setLevel_(NSFloatingWindowLevel)
        ns_window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces |
            NSWindowCollectionBehaviorFullScreenAuxiliary
        )
        ns_window.setHidesOnDeactivate_(False)
    except Exception as e:
        print("Floating window error:", e)

def ask_ai(prompt):
    import datetime
    try:
        with open(log_file, "a") as f:
            f.write(f"\n[{datetime.datetime.now()}] Sending prompt to Gemini: {prompt}\n")

        response = model.generate_content(prompt)

        result = response.text

        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Response: {result[:500]}\n")

        print("AI Response:", result)
        return result

    except Exception as e:
        print("Gemini Error:", e)
        return f"Error: {e}"

def main():
    app = QtWidgets.QApplication(sys.argv)
    panel = FloatingPanel()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
