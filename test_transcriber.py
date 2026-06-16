# test_transcriber.py

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from simple_transcriber import save_transcript, sanitize_title as sanitize_title_transcriber
from simple_download import download_audio, get_video_title, sanitize_title as sanitize_title_download
from simple_multi_download import read_url_list, sanitize_title as sanitize_title_multi
import subprocess


# ============================================================================
# TESTS FOR SAVE_TRANSCRIPT (Real function - not mocked logic)
# ============================================================================

def test_save_transcript(tmp_path):
    """Test that transcription text is saved correctly to a file."""
    text = "This is a test transcription in Spanish. El audio ha sido transcrito."
    output_path = tmp_path / "test_output.txt"
    
    save_transcript(text, path=output_path)

    assert output_path.exists(), "Output file was not created"
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert content == text, "Saved text does not match original"


def test_save_transcript_empty_text(tmp_path):
    """Test saving empty transcription."""
    text = ""
    output_path = tmp_path / "empty_test.txt"
    
    save_transcript(text, path=output_path)

    assert output_path.exists()
    assert output_path.stat().st_size == 0


def test_save_transcript_unicode(tmp_path):
    """Test saving transcription with special characters and accents."""
    text = "Hola, esto es una prueba con acentos: é, á, ö, ñ y emojis 🎉🎵"
    output_path = tmp_path / "unicode_test.txt"
    
    save_transcript(text, path=output_path)

    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        assert f.read() == text


# ============================================================================
# TESTS FOR SANITIZE_TITLE (Real function - all scripts)
# ============================================================================

class TestSanitizeTitle:
    """Test sanitize_title helper function across all scripts."""
    
    @pytest.mark.parametrize("input_title,expected", [
        ("Normal Title", "Normal Title"),
        ("Title@With#Special$Chars", "Title_With_Special_Chars"),
        ("Title/With/Slashes", "Title_With_Slashes"),
        ("123NumericTitle456", "123NumericTitle456"),
        ("Title-With-Dashes", "Title-With-Dashes"),
        ("Title_With_Underscores", "Title_With_Underscores"),
        ("MixedÑoñ@#$", "MixedÑoñ___"),
        ("   Leading and trailing   ", "   Leading and trailing   "),  # Spaces are allowed
        ("Title!@#$%^&*()", "Title__________"),
    ])
    def test_sanitize_title_download(self, input_title, expected):
        """Test sanitize_title from simple_download.py"""
        assert sanitize_title_download(input_title) == expected

    @pytest.mark.parametrize("input_title,expected", [
        ("Normal Title", "Normal Title"),
        ("Title@With#Special$Chars", "Title_With_Special_Chars"),
        ("Title/With/Slashes", "Title_With_Slashes"),
        ("MixedÑoñ@#$", "MixedÑoñ___"),
    ])
    def test_sanitize_title_transcriber(self, input_title, expected):
        """Test sanitize_title from simple_transcriber.py"""
        assert sanitize_title_transcriber(input_title) == expected

    @pytest.mark.parametrize("input_title,expected", [
        ("Normal Title", "Normal Title"),
        ("Title@With#Special$Chars", "Title_With_Special_Chars"),
        ("MixedÑoñ@#$", "MixedÑoñ___"),
    ])
    def test_sanitize_title_multi(self, input_title, expected):
        """Test sanitize_title from simple_multi_download.py"""
        assert sanitize_title_multi(input_title) == expected


# ============================================================================
# TESTS FOR get_video_title (Mocked subprocess)
# ============================================================================

@patch('simple_download.subprocess.run')
def test_get_video_title_success(mock_run):
    """Test getting video title from URL (mocked subprocess call)."""
    mock_result = MagicMock()
    mock_result.stdout = b"Test Video Title\n"
    mock_run.return_value = mock_result
    
    title = get_video_title("https://www.youtube.com/watch?v=TEST")
    
    assert title == "Test Video Title"
    assert mock_run.called
    # Verify the command includes yt-dlp
    args = mock_run.call_args[0][0]
    assert "yt-dlp" in args
    assert "--get-title" in args


@patch('simple_download.subprocess.run')
def test_get_video_title_failure(mock_run):
    """Test handling when video title fetch fails."""
    mock_run.side_effect = subprocess.CalledProcessError(1, "yt-dlp")
    
    with pytest.raises(RuntimeError, match="Failed to fetch title"):
        get_video_title("https://www.youtube.com/watch?v=INVALID")


@patch('simple_download.subprocess.run')
def test_get_video_title_with_unicode(mock_run):
    """Test getting title with special characters."""
    mock_result = MagicMock()
    mock_result.stdout = "Título en Español ñáéíóú".encode("latin-1")
    mock_run.return_value = mock_result
    
    title = get_video_title("https://www.youtube.com/watch?v=TEST")
    
    assert "ño" in title or "Español" in title


# ============================================================================
# TESTS FOR read_url_list (Real function)
# ============================================================================

def test_read_url_list(tmp_path):
    """Test reading URLs from list.txt file."""
    list_file = tmp_path / "test_list.txt"
    urls = [
        "https://www.youtube.com/watch?v=URL1",
        "https://www.youtube.com/watch?v=URL2",
        "https://www.youtube.com/watch?v=URL3",
    ]
    
    list_file.write_text("\n".join(urls), encoding="utf-8")
    
    read_urls = read_url_list(list_file)
    
    assert len(read_urls) == 3
    assert read_urls == urls


def test_read_url_list_with_empty_lines(tmp_path):
    """Test reading list file with empty lines and whitespace."""
    list_file = tmp_path / "test_list_blanks.txt"
    content = """https://www.youtube.com/watch?v=URL1

https://www.youtube.com/watch?v=URL2

    
https://www.youtube.com/watch?v=URL3"""
    
    list_file.write_text(content, encoding="utf-8")
    
    read_urls = read_url_list(list_file)
    
    # Should skip empty lines
    assert len(read_urls) == 3
    assert read_urls[0] == "https://www.youtube.com/watch?v=URL1"
    assert read_urls[1] == "https://www.youtube.com/watch?v=URL2"
    assert read_urls[2] == "https://www.youtube.com/watch?v=URL3"


def test_read_url_list_file_not_found():
    """Test reading from non-existent file returns empty list."""
    result = read_url_list("/nonexistent/path/file.txt")
    
    assert result == []


def test_read_url_list_empty_file(tmp_path):
    """Test reading from empty file."""
    list_file = tmp_path / "empty_list.txt"
    list_file.write_text("", encoding="utf-8")
    
    read_urls = read_url_list(list_file)
    
    assert read_urls == []


def test_read_url_list_only_whitespace(tmp_path):
    """Test file with only whitespace lines."""
    list_file = tmp_path / "whitespace_list.txt"
    list_file.write_text("   \n  \n\t\n", encoding="utf-8")
    
    read_urls = read_url_list(list_file)
    
    assert read_urls == []


# ============================================================================
# TESTS FOR download_audio (Mocked subprocess)
# ============================================================================

@patch('simple_download.subprocess.run')
def test_download_audio_success(mock_run):
    """Test successful audio download (mocked)."""
    mock_run.return_value = MagicMock()
    
    download_audio("https://www.youtube.com/watch?v=TEST", "/tmp")
    
    assert mock_run.called
    # Check that yt-dlp command was called with correct arguments
    args = mock_run.call_args[0][0]
    assert "yt-dlp" in args
    assert "-x" in args  # Audio extraction flag
    assert "--audio-format" in args
    assert "mp3" in args


@patch('simple_download.subprocess.run')
def test_download_audio_output_path_in_command(mock_run):
    """Test that output path is correctly passed to yt-dlp."""
    mock_run.return_value = MagicMock()
    test_path = "/home/user/videos"
    
    download_audio("https://www.youtube.com/watch?v=TEST", test_path)
    
    args = mock_run.call_args[0][0]
    # Find the output format argument
    assert any(test_path in arg for arg in args)


@patch('simple_download.subprocess.run')
def test_download_audio_failure(mock_run):
    """Test handling download failure."""
    mock_run.side_effect = subprocess.CalledProcessError(1, "yt-dlp")
    
    with pytest.raises(RuntimeError, match="Failed to download audio"):
        download_audio("https://www.youtube.com/watch?v=TEST", "/tmp")


# ============================================================================
# INTEGRATION TESTS (Logical workflows with mocked external dependencies)
# ============================================================================

def test_title_sanitization_workflow(tmp_path):
    """Test the workflow: get title → sanitize → create folder."""
    # Arrange: Simulate a video title with special characters
    video_title_raw = "Amazing Video! @#$% [2024]"
    
    # Act: Sanitize it using the real function
    safe_title = sanitize_title_download(video_title_raw)
    
    # Create folder using the safe title
    folder = tmp_path / safe_title
    folder.mkdir(parents=True, exist_ok=True)
    
    # Assert: Folder exists and has valid name
    assert folder.exists()
    assert folder.is_dir()
    # Verify no special characters in folder name
    assert "@" not in safe_title
    assert "#" not in safe_title
    assert "$" not in safe_title


def test_url_list_workflow(tmp_path):
    """Test the workflow: write URLs → read URLs → validate count."""
    # Arrange: Create a test list file
    list_file = tmp_path / "urls.txt"
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
    ]
    list_file.write_text("\n".join(urls), encoding="utf-8")
    
    # Act: Read URLs using the real function
    read_urls = read_url_list(list_file)
    
    # Assert: All URLs are read correctly
    assert len(read_urls) == len(urls)
    for expected_url, actual_url in zip(urls, read_urls):
        assert expected_url == actual_url


def test_transcript_save_with_sanitized_title(tmp_path):
    """Test saving transcript with a sanitized title."""
    # Arrange: Raw title and transcript
    raw_title = "Python Tutorial #1 - Basics!"
    transcript = "Welcome to the Python basics tutorial. Today we'll learn about variables."
    
    # Act: Sanitize title
    safe_title = sanitize_title_transcriber(raw_title)
    
    # Create transcript file
    transcript_file = tmp_path / f"{safe_title}.txt"
    save_transcript(transcript, transcript_file)
    
    # Assert: File exists and content is correct
    assert transcript_file.exists()
    with open(transcript_file, "r", encoding="utf-8") as f:
        assert f.read() == transcript
