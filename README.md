#  YT-to-Text 🎬→📝

**YT-to-Text** is a comprehensive Python suite of CLI tools for downloading audio from YouTube videos and transcribing them to text. It supports both single-video and batch processing with two transcription engines: **OpenAI Whisper** and **Faster-Whisper** (optimized for CPU performance).

---

##  🎯 Project Overview

This project is organized into modular, task-focused scripts:

- **Download Only** - Extract audio from YouTube URLs (single or batch)
- **Transcribe** - Download and transcribe audio to text (single or batch)
- **Batch Processing** - Process multiple videos from text files
- **Performance Optimized** - Use Faster-Whisper with INT8 quantization for faster transcription on CPU
- **Testing Included** - Unit tests for transcript validation and file handling

---

##  📊 Scripts Comparison

| Script | Purpose | Input | Output | Mode |
|--------|---------|-------|--------|------|
| `simple_download.py` | Download audio | Single YouTube URL | MP3 file | Single |
| `simple_multi_download.py` | Batch download | `list.txt` URLs | Multiple MP3s | Batch |
| `simple_transcriber.py` | Download + Transcribe | Single YouTube URL | MP3 + TXT | Single |
| `simple_multi_transcriber_Faster_Whisper.py` | Batch transcribe (optimized) | `transcriber.txt` URLs | Multiple MP3s + TXTs | Batch |

---

##  📋 Available Scripts

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

##  ⚙️ Requirements

Make sure you have the following installed:

- **Python 3.8+**
- **ffmpeg** - Required by yt-dlp for audio extraction
  - Windows: Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add to PATH
  - Or install via: `choco install ffmpeg` (if using Chocolatey)
  - Or via: `winget install FFmpeg`
  - Verify installation: `ffmpeg -version`

---

##  🚀 Installation & Setup

### Quick Start

1. **Clone or download this repository**

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   # or: source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify FFmpeg installation**:
   ```bash
   ffmpeg -version
   ```

### Preparing Input Files

For batch operations, create text files with YouTube URLs (one per line):

**For `simple_multi_download.py`:**
```
# Create list.txt with URLs:
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/watch?v=VIDEO_ID_3
```

**For `simple_multi_transcriber_Faster_Whisper.py`:**
```
# Create transcriber.txt with URLs:
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
```

---

##  ✨ Features

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

##  📁 Project Structure

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
├── .gitignore                                  # Git ignore rules
└── README.md                                   # This file
```

---

##  ⚙️ Advanced Configuration

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

##  🧪 Testing

Run the included unit tests:
```bash
python -m pytest test_transcriber.py -v
```

**Features tested:**
- Transcript file creation and encoding
- Empty transcript handling
- Unicode and special character support

---

##  🔧 Troubleshooting

### FFmpeg not found
**Error:** `ffmpeg: not found` or `[Errno 2] No such file or directory: 'ffmpeg'`
- **Solution:** Install FFmpeg and add it to your system PATH
  - Windows: `winget install FFmpeg` or download from ffmpeg.org
  - Verify: Open a new terminal and run `ffmpeg -version`

### YouTube URL not working
**Error:** `Failed to fetch title` or download fails
- **Solution:** 
  - Verify the URL is correct and the video is accessible
  - Check your internet connection
  - yt-dlp may need updates: `pip install --upgrade yt-dlp`

### Memory issues with large audio files
**Error:** Memory errors or slow transcription
- **Solution:**
  - Use Faster-Whisper instead of standard Whisper
  - Use smaller model size: `"base"` or `"small"` instead of `"medium"`
  - Process fewer videos at once

### Transcription not starting
**Error:** Model downloading seems stuck
- **Solution:**
  - First run downloads the Whisper model (can take time)
  - Check your internet connection
  - Models are cached locally after first download

---

##  📚 Dependencies & Versions

See `requirements.txt` for exact versions:

- **yt-dlp** - YouTube video/audio downloading
- **openai-whisper** - OpenAI's speech recognition model
- **faster-whisper** - Optimized Whisper implementation
- **tqdm** - Progress bars and visual feedback
- **pytest** - Testing framework
- **torch** - Machine learning framework (installed by Whisper)
- **numpy** - Numerical computing (installed by Whisper)
- **librosa** - Audio processing (installed by Whisper)

---

##  📄 License & Contributing

Created by **Eugenio**

Feel free to fork, modify, and adapt this project for your needs.

##  Support

For issues with FFmpeg installation or other dependencies, refer to:
- [FFmpeg Official Guide](https://ffmpeg.org/documentation.html)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Whisper GitHub](https://github.com/openai/whisper)
- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
