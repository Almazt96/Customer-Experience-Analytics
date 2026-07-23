# Unit tests for cleaning & tokenization
# Automated Unit Testing
import pytest
from src.text_processor import TextPreprocessor

def test_clean_text_removes_urls():
    raw_text = "Great app! Check http://example.com for more info."
    cleaned = TextPreprocessor.clean_text(raw_text)
    assert "http://example.com" not in cleaned
    assert "Great app!" in cleaned

def test_clean_text_handles_none():
    assert TextPreprocessor.clean_text(None) == ""

def test_clean_text_handles_special_characters():
    raw_text = "CBE App is slow!!! 🔥🔥🔥"
    cleaned = TextPreprocessor.clean_text(raw_text)
    assert "🔥" not in cleaned
    assert "CBE App is slow!!!" in cleaned