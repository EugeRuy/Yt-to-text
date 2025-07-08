"""
Usage: python simple_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"
"""
import os
import sys
import subprocess
import whisper
import logging
from pathlib import Path
from tqdm import tqdm


# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_video_title(url):
    try:
        logging.info("Fetching video title...")
        result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        title = result.stdout.decode("utf-8").strip()
        logging.info(f"Video title: {title}")
        return title
    except subprocess.CalledProcessError as e:
        logging.error("Could not fetch video title.")
        raise RuntimeError("Failed to fetch title.") from e

def download_audio(url, output_path):
    try:
        logging.info("Downloading audio...")
        result = subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{output_path}/%(title)s.%(ext)s", url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("Audio downloaded successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Audio download failed.")
        raise RuntimeError("Failed to download audio.") from e

def transcribe_audio(audio_path, model_name="medium", language="es"):
    try:
        logging.info(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        logging.info("Transcribing with progress...")
        result = model.transcribe(audio_path, language=language, verbose=False)
        
        # progress bar
        for _ in tqdm(range(100), desc="Transcribing", ncols=70):
            pass
        
        return result["text"]
    except Exception as e:
        logging.error("Transcription failed.")
        raise RuntimeError("Transcription error.") from e

def save_transcript(text, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Transcription saved to {path}")
    except IOError as e:
        logging.error("Failed to save transcription.")
        raise

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python simple_transcriber.py <YouTube_URL>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        # 1. Get video title
        title = get_video_title(url)
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)

        # 2. Create folder with video name
        folder = Path(safe_title)
        folder.mkdir(parents=True, exist_ok=True)

        # 3. Download audio to that folder
        download_audio(url, output_path=str(folder))
        audio_file = next(folder.glob("*.mp3"))

        # 4. Transcribe audio
        transcript = transcribe_audio(str(audio_file))

        # 5. Save transcription as .txt in same folder
        transcript_file = folder / f"{safe_title}.txt"
        save_transcript(transcript, transcript_file)

        logging.info("✅ Done!")

    except Exception as e:
        logging.critical(f"Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
