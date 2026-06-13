"""
Usage: python simple_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
"""

import sys
import subprocess
import logging
from pathlib import Path


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
        title = result.stdout.decode("latin-1").strip()
        logging.info(f"Video title: {title}")
        return title
    except subprocess.CalledProcessError as e:
        logging.error("Could not fetch video title.")
        raise RuntimeError("Failed to fetch title.") from e


def sanitize_title(title):
    """Convert a video title to a safe folder name."""
    return "".join(
        c if c.isalnum() or c in " -_" else "_"
        for c in title
    )


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
        raise RuntimeError("Failed to download audio.") from e


def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python simple_audio_downloader.py <YouTube_URL>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        # 1. Get video title
        title = get_video_title(url)
        safe_title = sanitize_title(title)

        # 2. Create folder with video name
        folder = Path(safe_title)
        folder.mkdir(parents=True, exist_ok=True)

        # 3. Download audio to that folder
        download_audio(url, output_path=str(folder))

        logging.info("✅ Done!")

    except Exception as e:
        logging.critical(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()