# 📷 SnapAI

**SnapAI** is a lightweight floating panel app for **macOS** that monitors your screenshots, extracts text using OCR, and sends it to the **Groq LLaMA 3 API** to generate intelligent answers.

Perfect for answering quizzes, fill-in-the-blank questions, and MCQs automatically using screenshots.

---

## ✨ Features

- 📸 Automatically detects new screenshots from `~/Downloads`
- 🧠 Extracts text using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 💬 Sends extracted text to Groq’s **LLaMA 3** model via API
- 🪟 Beautiful floating, draggable, semi-transparent UI
- ✅ Buttons to Start / Stop / Quit
- 📋 All logs saved to `~/snapai_log.txt`

---

## ⚙️ Setup Instructions

### 1. Open Terminal
Press Cmd + Space, type Terminal, and press Enter.

### 2. Navigate to the folder where you want to clone the repo
For example, your Desktop:

```bash
cd ~/Desktop
```

### 3. Clone this Repository

```bash
git clone https://github.com/MK-0406/SnapAI_Mac.git
cd SnapAI_Mac
```

### 4. Get a Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up or log in with your account.
3. Click "Create API Key"
4. Copy the key (starts with gsk_...)

### 5. Create a `.env` file with your API key:

```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 6. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 7. Run the app:

```bash
python3 SnapAI.py
```

---

## Requirements

- macOS
- Tesseract OCR
- Python 3.8 or later

1. Tesseract must be installed separately:
  
```bash
brew install tesseract  # macOS
```

2. Make sure Tesseract is in your system PATH or edit SnapAI.py:

```python
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # for Apple Silicon
```

