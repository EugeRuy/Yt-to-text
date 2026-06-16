"""
Usage: python multy_transcriber_local.py

Reads URLs from transcriber.txt (one per line).
Downloads audio, transcribes, saves all .txt files to a single 'Textos' folder,
then deletes the audio file.
creado con google/gemma-4-12b-qat
"""

import subprocess
import logging
import shutil
from pathlib import Path
from faster_whisper import WhisperModel

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

LIST_FILE = "transcriber.txt"
OUTPUT_FOLDER = Path("Textos")
TEMP_FOLDER = Path("temp_audio_download")

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

def sanitize_title(title):
    return "".join(
        c if c.isalnum() or c in " -_" else "_"
        for c in title
    )

def transcribe_audio(audio_path, model):
    try:
        logging.info("Transcribing...")
        segments, info = model.transcribe(
            audio_path,
            language="es",
            beam_size=5,
            log_progress=True
        )

        full_text = ""
        for segment in segments:
            full_text += segment.text + " "

        return full_text.strip()
    except Exception as e:
        logging.error(f"Transcription failed: {str(e)}")
        raise

def save_transcript(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    logging.info(f"Transcription saved to {path}")

def process_url(url, model):
    try:
        # 1. Crear carpeta de salida si no existe
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        
        # 2. Crear carpeta temporal para el audio
        TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

        title = get_video_title(url)
        safe_title = sanitize_title(title)

        # 3. Descargar audio a la carpeta temporal
        download_audio(url, output_path=str(TEMP_FOLDER))

        # 4. Buscar el archivo de audio descargado
        audio_extensions = ('*.mp3', '*.m4a', '*.wav', '*.flac', '*.opus', '*.ogg')
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(TEMP_FOLDER.glob(ext))
        
        if not audio_files:
            audio_files = [f for f in TEMP_FOLDER.glob('*') if f.is_file() and f.suffix != '.txt']
        
        if not audio_files:
            raise RuntimeError(f"No audio file found in {TEMP_FOLDER}")
        
        audio_file = audio_files[0]
        logging.info(f"Found audio file: {audio_file.name}")

        # 5. Transcribir
        transcript = transcribe_audio(str(audio_file), model)

        # 6. Guardar el texto en la carpeta "Textos"
        transcript_file = OUTPUT_FOLDER / f"{safe_title}.txt"
        save_transcript(transcript, transcript_file)

        # 7. LIMPIEZA: Borrar el contenido de la carpeta temporal
        for file in TEMP_FOLDER.iterdir():
            if file.is_file():
                file.unlink()
        
        logging.info(f"✅ Finished: {safe_title}\n")

    except Exception as e:
        logging.exception(f"❌ Error processing {url}\n")
    finally:
        # Asegurarse de que la carpeta temporal esté vacía al final de cada proceso
        try:
            for file in TEMP_FOLDER.iterdir():
                if file.is_file():
                    file.unlink()
        except:
            pass

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

    logging.info("Loading Faster-Whisper model (small, INT8, CPU)...")

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    for index, url in enumerate(urls, start=1):
        logging.info(f"Processing ({index}/{len(urls)})")
        process_url(url, model)

    logging.info("🎉 All transcriptions processed.")

if __name__ == "__main__":
    main()
