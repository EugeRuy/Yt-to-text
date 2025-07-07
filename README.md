# Simple YouTube to Text Transcriber

A lightweight Python script that downloads YouTube videos, extracts audio, and transcribes them to text using OpenAI's Whisper model.

## Features

- 🎬 Download YouTube videos as audio (MP3)
- 🎤 Transcribe audio to text using Whisper
- 📁 Organize files in a single folder named after the video
- 🌍 Supports multiple languages (default: Spanish)
- ⚡ Simple command-line interface

## Requirements

- Python 3.8 or higher
- FFmpeg installed and available in PATH
- Virtual environment (recommended)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd yt-to-text
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\Activate.ps1
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python simple_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Example
```bash
python simple_transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Output

The script creates a folder named after the video containing:
- `Video_Title.mp3` - Downloaded audio file
- `Video_Title.txt` - Transcribed text

## Configuration

### Model Size
The script uses Whisper's "medium" model by default. You can modify the model size in the script:
- `tiny` - Fastest, least accurate
- `base` - Fast, good for short videos
- `small` - Balanced speed/accuracy
- `medium` - Good accuracy (default)
- `large` - Best accuracy, slowest

### Language
Default language is Spanish. Change the `language` parameter in the `transcribe_audio` function call.

## Troubleshooting

### FFmpeg Issues
If you get FFmpeg-related errors:
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add FFmpeg to your system PATH
3. Restart your terminal

### Import Errors
Make sure you're using the virtual environment:
```bash
# Check if virtual environment is active (should show (.venv) in prompt)
# If not, activate it:
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux
```

### Dependencies
If you get module not found errors:
```bash
pip install -r requirements.txt
```

## Dependencies

- `yt-dlp` - YouTube video downloading
- `openai-whisper` - Audio transcription
- `ffmpeg-python` - Audio processing

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 