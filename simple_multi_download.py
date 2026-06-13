"""
Usage: python simple_multi_download.py

The script reads URLs from list.txt (one per line)
"""

import subprocess
import logging
from pathlib import Path


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)


LIST_FILE = "list.txt"


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
        logging.info("Download completed.")
    except Exception as e:
        logging.error("Audio download failed.")
        raise RuntimeError("Download failed") from e


def sanitize_title(title):
    """Convert a video title to a safe folder name."""
    return "".join(
        c if c.isalnum() or c in " -_" else "_"
        for c in title
    )


def read_url_list(file_path):
    """Read URLs from a text file (one per line).
    
    Args:
        file_path: Path to the text file containing URLs
        
    Returns:
        List of URLs (empty lines are skipped)
    """
    path = Path(file_path)
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def process_url(url):
    try:
        title = get_video_title(url)
        safe_title = sanitize_title(title)

        folder = Path(safe_title)
        folder.mkdir(parents=True, exist_ok=True)

        download_audio(url, output_path=str(folder))

        logging.info(f"✅ Finished: {safe_title}\n")

    except Exception as e:
        logging.error(f"❌ Error processing {url}: {e}\n")


def main():
    urls = read_url_list(LIST_FILE)

    if not urls:
        logging.critical(f"No URLs found in {LIST_FILE}")
        return

    logging.info(f"Found {len(urls)} URLs.\n")

    for index, url in enumerate(urls, start=1):
        logging.info(f"Processing ({index}/{len(urls)})")
        process_url(url)

    logging.info("🎉 All downloads processed.")


if __name__ == "__main__":
    main()