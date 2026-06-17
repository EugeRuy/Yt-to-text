# YT-to-Text

A Python suite of CLI tools for downloading audio from YouTube videos and transcribing them to text. Supports single-video and batch processing with two transcription engines: **OpenAI Whisper** and **Faster-Whisper** (CPU-optimized with INT8 quantization).

---

## Features

- **Channel Link Extraction** — Scrape all video/stream URLs from a YouTube channel
- **Link Splitting** — Split large URL lists into smaller chunks for batch processing
- **Audio Download** — Download MP3 from YouTube via `yt-dlp` (single or batch)
- **Transcription** — Transcribe audio to text using Whisper or Faster-Whisper
- **Batch Processing** — Process multiple videos sequentially with a single model load
- **Flexible Output** — Save transcripts in per-video folders or a single output directory
- **CPU Optimized** — Faster-Whisper with INT8 quantization for efficient CPU inference
- **Unit Tests** — Validation for transcription, title sanitization, and file handling

---

## Scripts Overview

| Script | Description | Input | Output |
|--------|-------------|-------|--------|
| `get_links_youtube.py` | Extract all video/stream URLs from YouTube channels | `Canales.txt` | `Linksvideos.txt` |
| `split_links.py` | Split a URL list into smaller chunk files | `Convertir/<file>.txt` | `Convertir/output/N.txt` |
| `simple_download.py` | Download audio from a single video | CLI URL argument | `{title}/{title}.mp3` |
| `simple_multi_download.py` | Batch download audio from a URL list | `list.txt` | Per-video folders with MP3 |
| `simple_transcriber.py` | Download + transcribe a single video (Whisper) | CLI URL argument | `{title}/{title}.mp3` + `{title}/{title}.txt` |
| `simple_multi_transcriber.py` | Batch download + transcribe (Whisper, model reused) | `transcriber.txt` | Per-video folders with MP3 + TXT |
| `simple_multi_transcriber_Faster_Whispe.py` | Batch download + transcribe (Faster-Whisper, CPU) | `transcriber.txt` | Per-video folders with MP3 + TXT |
| `multy_transcriber_1Folder.py` | Batch transcribe (Faster-Whisper), all texts in `Textos/`, audio deleted | `transcriber.txt` | `Textos/{title}.txt` |
| `multy_transcriber_local.py` | Batch transcribe (Faster-Whisper), texts in `Textos/`, temp audio cleaned up | `transcriber.txt` | `Textos/{title}.txt` |

---

## Detailed Script Usage

### 1. `get_links_youtube.py` — Extract Channel Links

Scrapes all video and livestream URLs from YouTube channels listed in `Canales.txt`.

```bash
python get_links_youtube.py
```

- Reads channels from `Canales.txt` (one URL per line, e.g. `https://www.youtube.com/@channelname`)
- Saves extracted URLs to `Linksvideos.txt` (appends new links on re-run)
- Skips already saved links; no duplicates

### 2. `split_links.py` — Split URL Lists

Divides a single `.txt` file inside the `Convertir/` folder into smaller chunk files.

```bash
python split_links.py
python split_links.py --carpeta "MyFolder" --chunk 20
```

- Expects exactly one `.txt` file in `Convertir/`
- Splits it into files of 10 URLs each (default) inside `Convertir/output/`

### 3. `simple_download.py` — Single Video Download

```bash
python simple_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Downloads audio as MP3 into a folder named after the video title.

### 4. `simple_multi_download.py` — Batch Download

```bash
python simple_multi_download.py
```

Reads URLs from `list.txt` (one per line). Each video's audio is saved in its own folder.

### 5. `simple_transcriber.py` — Single Video Transcribe (Whisper)

```bash
python simple_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Downloads audio and transcribes it using OpenAI Whisper (`medium` model, Spanish). Outputs both `.mp3` and `.txt` in a video-named folder.

### 6. `simple_multi_transcriber.py` — Batch Transcribe (Whisper)

```bash
python simple_multi_transcriber.py
```

Reads URLs from `transcriber.txt`, loads the Whisper `medium` model once, and transcribes all videos sequentially.

### 7. `simple_multi_transcriber_Faster_Whispe.py` — Batch Transcribe (Faster-Whisper)

```bash
python simple_multi_transcriber_Faster_Whispe.py
```

Same batch workflow as above but uses **Faster-Whisper** with the `small` model and INT8 quantization for faster CPU inference.

### 8. `multy_transcriber_1Folder.py` — Batch Transcribe, Single Output Folder

```bash
python multy_transcriber_1Folder.py
```

Transcribes all videos from `transcriber.txt` using Faster-Whisper, saves all `.txt` files into the `Textos/` folder, and deletes the downloaded audio after each video.

### 9. `multy_transcriber_local.py` — Batch Transcribe, Single Output Folder (v2)

```bash
python multy_transcriber_local.py
```

Same as above but with a dedicated temp folder (`temp_audio_download/`) for audio files that is cleaned up after each video. All transcripts go to `Textos/`.

---

## Requirements

- **Python 3.8+**
- **FFmpeg** — Required by yt-dlp for audio extraction
  - Windows: `winget install FFmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - Verify: `ffmpeg -version`

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/YT-to-Text.git
cd YT-to-Text

# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate     # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Verify FFmpeg is available
ffmpeg -version
```

---

## Input File Setup

| File | Used By | Format |
|------|---------|--------|
| `Canales.txt` | `get_links_youtube.py` | One channel URL per line |
| `list.txt` | `simple_multi_download.py` | One video URL per line |
| `transcriber.txt` | All transcribe scripts | One video URL per line |

---

## Project Structure

```
YT-to-Text/
├── get_links_youtube.py                  # Channel link extraction
├── split_links.py                        # URL list splitting
├── simple_download.py                    # Single video download
├── simple_multi_download.py              # Batch video download
├── simple_transcriber.py                 # Single transcribe (Whisper)
├── simple_multi_transcriber.py           # Batch transcribe (Whisper)
├── simple_multi_transcriber_Faster_Whispe.py  # Batch transcribe (Faster-Whisper)
├── multy_transcriber_1Folder.py          # Batch transcribe, single output folder
├── multy_transcriber_local.py            # Batch transcribe, single output folder (v2)
├── test_transcriber.py                   # Unit tests
├── Canales.txt                           # Channel URLs input
├── list.txt                              # Download list input
├── transcriber.txt                       # Transcribe list input
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore rules
└── README.md                             # This file
```

---

## Advanced Configuration

### Change Language

Edit the `language` parameter in any transcribe script:

```python
# Whisper (simple_transcriber.py, simple_multi_transcriber.py)
result = model.transcribe(audio_path, language="en", verbose=False)

# Faster-Whisper (simple_multi_transcriber_Faster_Whispe.py, etc.)
segments, info = model.transcribe(audio_path, language="en", beam_size=5)
```

Common codes: `en` (English), `es` (Spanish), `fr` (French), `de` (German), `ja` (Japanese).

### Change Model Size

- **Whisper scripts**: Change `model_name="medium"` to: `tiny`, `base`, `small`, `medium`, `large`
- **Faster-Whisper scripts**: Change `"small"` to: `tiny`, `base`, `small`, `medium`, `large-v3`

---

## Testing

```bash
python -m pytest test_transcriber.py -v
```

Tests cover: transcript file creation, empty transcript handling, Unicode support, title sanitization, URL list reading, mocked download/title fetch, and integration workflows.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ffmpeg not found` | Install FFmpeg and add it to your PATH |
| YouTube download fails | Check URL validity, internet connection, update yt-dlp: `pip install --upgrade yt-dlp` |
| Slow transcription | Use Faster-Whisper or a smaller model (`small`, `base`, `tiny`) |
| Model download stuck | First run downloads the model; it is cached locally afterwards |

---

## Dependencies

- **yt-dlp** — YouTube audio downloading
- **openai-whisper** — OpenAI speech recognition
- **faster-whisper** — Optimized Whisper implementation
- **tqdm** — Progress bars
- **pytest** — Testing framework

External: **FFmpeg** (required by yt-dlp).

---

## License

Created by **Eugenio**. Feel free to fork, modify, and adapt.
