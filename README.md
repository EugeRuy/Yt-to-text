# 🎧 YT-to-Text

**YT-to-Text** is a simple CLI tool that downloads audio from a YouTube video and transcribes it using [OpenAI Whisper](https://github.com/openai/whisper).

It saves both the audio (`.mp3`) and the transcription (`.txt`) inside a folder named after the video title.

---

## ✨ Features

- ✅ Automatically downloads and extracts audio from a YouTube URL using `yt-dlp`
- ✅ Transcribes audio to text using OpenAI's `whisper`
- ✅ Organizes files into a folder with the video title
- ✅ Applies error handling and logging for robustness
- ✅ Displays a transcription progress bar (via `tqdm`)
- ✅ Includes unit tests

---

## 📦 Requirements

Make sure you have the following installed:

- Python 3.8+
- `ffmpeg` installed and available in your system PATH  
  👉 [Download FFmpeg](https://ffmpeg.org/download.html)

Then install the dependencies with:

```bash
pip install -r requirements.txt
