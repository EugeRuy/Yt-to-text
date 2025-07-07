#!/usr/bin/env python3
"""
Simple YouTube to Text Transcriber
Usage: python simple_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"
"""

import os
import sys
import whisper
import re
import yt_dlp
from pathlib import Path

def sanitize_filename(filename):
    """Make filename safe for filesystem."""
    # Remove all problematic characters including #
    filename = re.sub(r'[<>:"/\\|?*#]', '_', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename[:100] if len(filename) > 100 else filename

def get_video_title(youtube_url):
    """Extract video title using yt-dlp."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            if info is None:
                return None
            return info.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Error getting video title: {e}")
        return None

def download_and_transcribe(youtube_url):
    """Download audio and transcribe in one step."""
    print("🔍 Getting video title...")
    title = get_video_title(youtube_url)
    if not title:
        print("❌ Could not get video title")
        return None
    
    safe_title = sanitize_filename(title)
    folder_name = safe_title
    
    print(f"📁 Creating folder: {folder_name}")
    os.makedirs(folder_name, exist_ok=True)
    
    # Download audio directly to the folder
    print("⬇️ Downloading audio...")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(folder_name, f'{safe_title}.%(ext)s'),
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # Find the downloaded audio file
        audio_file = None
        for file in os.listdir(folder_name):
            if file.endswith('.mp3'):
                audio_file = os.path.join(folder_name, file)
                break
        
        if not audio_file:
            print("❌ Audio file not found after download")
            return None
            
        print(f"✅ Audio downloaded: {audio_file}")
        
        # Transcribe
        print("🎤 Transcribing audio...")
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file, language="Spanish", verbose=False)
        
        # Save transcript
        transcript_file = os.path.join(folder_name, f"{safe_title}.txt")
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print(f"✅ Transcript saved: {transcript_file}")
        print(f"📂 All files saved in folder: {folder_name}")
        
        return transcript_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python simple_transcriber.py \"https://www.youtube.com/watch?v=VIDEO_ID\"")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    print(f"🎬 Processing: {youtube_url}")
    
    result = download_and_transcribe(youtube_url)
    if result:
        print("🎉 Success! Check the created folder for your files.")
    else:
        print("💥 Failed to process video.")
        sys.exit(1)

if __name__ == "__main__":
    main() 