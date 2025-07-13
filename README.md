# TinyClip 🎬

**TinyClip** is a minimalist web-based tool to compress your videos quickly and efficiently — perfect for sharing on platforms like Discord without Nitro (<10MB).  
No logs, no file storage, pure client-to-server streaming with optional speed-up and precise size targeting.

---

## 🚀 Features

- 🎯 Target final file size (in MB)
- ⚡ Speed up the video (optional)
- 🧠 Automatic 2-pass encoding via `ffmpeg`
- 🕵️ No file logging or storage (privacy-first)
- 🖥️ Built on Python + Flask (lightweight backend)

---

## 📦 How It Works

1. Upload your video file via the interface.
2. Select your target size (e.g. 8 MB) and optional playback speed (e.g. 1.25x).
3. Wait for compression to finish.
4. Download your optimized video.

---

## 🧪 Technologies Used

- Python 3.11+
- Flask (Backend API)
- ffmpeg (CLI compression)
- HTML/JS Frontend (one-page UI)
- No database, no persistent storage

---

## ⚙️ Running Locally

```bash
git clone https://github.com/yourname/tinyclip.git
cd tinyclip

# Set up virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Make sure `ffmpeg` is installed and available in your PATH.

---

## 🛡️ Disclaimer

TinyClip is designed with privacy in mind — it does not log or retain any files. However, always use trusted servers for sensitive media.

---

## 📫 Contact

Made with ❤️ by Naorah  
Project #9 – From script to web 🧩

---

## 📃 License

MIT License