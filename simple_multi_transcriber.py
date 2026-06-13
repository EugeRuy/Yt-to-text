"""
Usage: python simple_multi_transcriber.py

The script reads URLs from transcriber.txt (one per line)
"""

import subprocess
import logging
from pathlib import Path
import whisper
from tqdm import tqdm


# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

LIST_FILE = "transcriber.txt"


def get_video_title(url):
    try:
        logging.info(f"Fetching title for: {url}")
        result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        title = result.stdout.decode("latin-1").strip()
        return title
    except subprocess.CalledProcessError:
        logging.error(f"Failed to fetch title for {url}")
        raise RuntimeError("Title fetch failed")


def download_audio(url, output_path):
    try:
        logging.info("Downloading audio...")
        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "-o", f"{output_path}/%(title)s.%(ext)s",
                url
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("Audio downloaded successfully.")
    except Exception as e:
        logging.error("Audio download failed.")
        raise RuntimeError("Download failed") from e


def transcribe_audio(audio_path, model):
    try:
        logging.info("Transcribing...")
        result = model.transcribe(audio_path, language="es", verbose=False)

        # Visual progress placeholder (igual que tu script original)
        for _ in tqdm(range(100), desc="Transcribing", ncols=70):
            pass

        return result["text"]
    except Exception as e:
        logging.error(f"Transcription failed: {str(e)}")
        raise


def save_transcript(text, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Transcription saved to {path}")
    except IOError:
        logging.error("Failed to save transcription.")
        raise


def sanitize_title(title):
    return "".join(
        c if c.isalnum() or c in " -_" else "_"
        for c in title
    )


def process_url(url, model):
    try:
        title = get_video_title(url)
        safe_title = sanitize_title(title)

        folder = Path(safe_title)
        folder.mkdir(parents=True, exist_ok=True)

        download_audio(url, output_path=str(folder))

        # Buscar cualquier archivo de audio (mp3, m4a, wav, etc.)
        audio_extensions = ('*.mp3', '*.m4a', '*.wav', '*.flac', '*.opus', '*.ogg')
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(folder.glob(ext))
        
        if not audio_files:
            # Si no encuentra con extensiones específicas, busca todos los archivos excepto .txt
            audio_files = [f for f in folder.glob('*') if f.is_file() and f.suffix != '.txt']
        
        if not audio_files:
            raise RuntimeError(f"No audio file found in {folder}")
        audio_file = audio_files[0]
        logging.info(f"Found audio file: {audio_file.name}")

        transcript = transcribe_audio(str(audio_file), model)

        transcript_file = folder / f"{safe_title}.txt"
        save_transcript(transcript, transcript_file)

        logging.info(f"✅ Finished: {safe_title}\n")

    except Exception as e:
        logging.exception(f"❌ Error processing {url}\n")


def main():
    list_path = Path(LIST_FILE)

    if not list_path.exists():
        logging.critical(f"{LIST_FILE} not found.")
        return

    urls = [
        line.strip()
        for line in list_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not urls:
        logging.warning("No URLs found in transcriber.txt")
        return

    logging.info(f"Found {len(urls)} URLs.\n")

    # 🔥 Cargar modelo UNA sola vez (clave para rendimiento)
    logging.info("Loading Whisper model (medium)...")
    model = whisper.load_model("medium")

    for index, url in enumerate(urls, start=1):
        logging.info(f"Processing ({index}/{len(urls)})")
        process_url(url, model)

    logging.info("🎉 All transcriptions processed.")


if __name__ == "__main__":
    main()