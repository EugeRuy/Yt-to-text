# test_transcriber.py

import pytest
from simple_transcriber import save_transcript

def test_save_transcript(tmp_path):
    text = "This is a test - transcription test."
    output_path = tmp_path / "test_output.txt"
    
    save_transcript(text, path=output_path)

    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        assert f.read() == text
