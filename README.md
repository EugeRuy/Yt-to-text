#  YT-to-Text

**YT-to-Text** is a comprehensive Python suite of CLI tools for downloading audio from YouTube videos and transcribing them to text. It supports both single-video and batch processing with two transcription engines: **OpenAI Whisper** and **Faster-Whisper** (optimized for CPU performance).

---

##  Project Overview

This project is organized into modular, task-focused scripts:

- **Download Only** - Extract audio from YouTube URLs (single or batch)
- **Transcribe** - Download and transcribe audio to text (single or batch)
- **Batch Processing** - Process multiple videos from text files
- **Performance Optimized** - Use Faster-Whisper with INT8 quantization for faster transcription on CPU

---

##  Available Scripts

### 1. **simple_download.py** - Single Video Audio Download
Downloads audio from a single YouTube URL and saves it as an MP3 file. 

**Usage:**
```bash
python simple_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**What it does:**
- Fetches the video title
- Creates a folder named after the video
- Downloads the audio in MP3 format
- Saves to `{video_title}/{video_title}.mp3`

---

### 2. **simple_multi_download.py** - Batch Audio Download
Downloads audio from multiple YouTube URLs listed in a text file.

**Usage:**
```bash
python simple_multi_download.py
```

**Configuration:**
- Reads URLs from `list.txt` (one URL per line)

**What it does:**
- Processes each URL in `list.txt` sequentially
- Fetches video title for each URL
- Creates a folder for each video
- Downloads audio in MP3 format
- Displays progress and error handling for each video

---

### 3. **simple_transcriber.py** - Single Video Download & Transcription
Downloads audio from a YouTube URL and transcribes it to text using OpenAI Whisper.

**Usage:**
```bash
python simple_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**What it does:**
- Fetches the video title
- Creates a folder named after the video
- Downloads the audio in MP3 format
- **Transcribes audio to text** using Whisper (Spanish language)
- Saves both audio and transcript:
  - `{video_title}/{video_title}.mp3`
  - `{video_title}/{video_title}.txt`

**Features:**
- Uses Whisper "medium" model by default
- Configured for Spanish transcription
- Shows transcription progress bar
- Robust error handling and logging

---

### 4. **simple_multi_transcriber_Faster_Whisper.py** - Batch Download & Transcription (Optimized)
Downloads audio and transcribes text from multiple YouTube URLs using **Faster-Whisper** with CPU optimization.

**Usage:**
```bash
python simple_multi_transcriber_Faster_Whisper.py
```

**Configuration:**
- Reads URLs from `transcriber.txt` (one URL per line)

**What it does:**
- Processes each URL in `transcriber.txt` sequentially
- Fetches video title for each URL
- Creates a folder for each video
- Downloads the audio in MP3 format
- **Transcribes audio to text** using Faster-Whisper
- Saves both audio and transcript:
  - `{video_title}/{video_title}.mp3`
  - `{video_title}/{video_title}.txt`

**Features:**
- Uses **Faster-Whisper** (faster inference than standard Whisper)
- Whisper "medium" model with **INT8 quantization** for CPU optimization
- Configured for Spanish transcription
- Beam size of 5 for balanced accuracy/speed
- Processes multiple URLs in batch with detailed logging
- Error handling and progress tracking per video
- Loads model once, reuses for all videos in batch

**Performance Benefits:**
- INT8 quantization reduces model size and memory usage
- CPU-optimized execution
- Reuses model across batch processing (faster for multiple videos)

---

##  Requirements

Make sure you have the following installed:

- **Python 3.8+**
- **ffmpeg** - Required by yt-dlp for audio extraction
  - Windows: Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add to PATH
  - Or install via: `choco install ffmpeg` (if using Chocolatey)
  - Or via: `winget install FFmpeg`

---

##  Installation

1. **Clone the repository** (or download the files)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

##  Features

- ✅ **Single & Batch Processing** - Download/transcribe one video or multiple videos
- ✅ **Audio Extraction** - Extract MP3 from YouTube using `yt-dlp`
- ✅ **Dual Transcription Engines**:
  - OpenAI Whisper (simple_transcriber.py)
  - Faster-Whisper with INT8 optimization (simple_multi_transcriber_Faster_Whisper.py)
- ✅ **Spanish Transcription** - Configured for Spanish language by default
- ✅ **Smart Organization** - Creates folders named after video titles
- ✅ **Comprehensive Logging** - Detailed console output and error messages
- ✅ **Progress Tracking** - Visual feedback during processing
- ✅ **Error Handling** - Graceful handling of network and processing errors
- ✅ **Batch Reusability** - Whisper model loaded once for batch jobs (performance optimization)
- ✅ **Unit Tests** - Included test file for validation

---

##  Project Structure

```
YT-to-Text/
├── simple_download.py                          # Single video audio download
├── simple_multi_download.py                    # Batch audio download
├── simple_transcriber.py                       # Single video download + transcribe
├── simple_multi_transcriber_Faster_Whisper.py # Batch download + transcribe (optimized)
├── test_transcriber.py                         # Unit tests
├── list.txt                                    # URL list for batch download
├── transcriber.txt                             # URL list for batch transcription
├── requirements.txt                            # Python dependencies
└── README.md                                   # This file
```

---

##  Dependencies

Key packages used in this project:

- **yt-dlp** - Download videos from YouTube
- **openai-whisper** - Speech-to-text transcription
- **faster-whisper** - Optimized Whisper implementation
- **ffmpeg-python** - FFmpeg wrapper for audio processing
- **tqdm** - Progress bars and visual feedback
- **pytest** - Testing framework
- **torch** - Machine learning framework (for Whisper models)
- **transformers** - NLP models and utilities

See `requirements.txt` for the complete list with versions.

---

##  Advanced Configuration

### Change Transcription Language
Edit the language parameter in the scripts:
- In `simple_transcriber.py`: Change `language="es"` to another language code
- In `simple_multi_transcriber_Faster_Whisper.py`: Change `language="es"` to another language code

Common language codes: `en` (English), `es` (Spanish), `fr` (French), `de` (German), `ja` (Japanese), etc.

### Change Whisper Model Size
In `simple_transcriber.py`: Change `model_name="medium"` to:
- `"tiny"` - Fastest, least accurate
- `"base"` - Fast, reasonable accuracy
- `"small"` - Balanced speed/accuracy
- `"medium"` - Higher accuracy, slower
- `"large"` - Highest accuracy, slowest

---

##  Testing

Run the included unit tests:
```bash
python -m pytest test_transcriber.py
```

---

##  License

Created by Eugenio

---

##  Contributing

Feel free to fork, modify, and adapt this project for your needs.

---

##  Support

For issues with FFmpeg installation or other dependencies, refer to:
- [FFmpeg Official Guide](https://ffmpeg.org/documentation.html)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Whisper GitHub](https://github.com/openai/whisper)
- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
