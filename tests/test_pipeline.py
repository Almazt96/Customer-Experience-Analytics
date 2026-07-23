import pytest
import pandas as pd
from src.text_processor import TextPreprocessor

@pytest.fixture
def sample_reviews():
    return [
        "CBE App is fast and reliable! 5 stars",
        "OTP not received for 2 days... http://help.link",
        None,
        ""
    ]

def test_clean_text_url_removal():
    raw = "Check http://example.com for info"
    cleaned = TextPreprocessor.clean_text(raw)
    assert "http://example.com" not in cleaned

def test_clean_text_handles_none_and_empty():
    assert TextPreprocessor.clean_text(None) == ""
    assert TextPreprocessor.clean_text("") == ""

def test_clean_text_preserves_alphanumeric():
    raw = "Dashen bank transfer failed! #error"
    cleaned = TextPreprocessor.clean_text(raw)
    assert "Dashen bank transfer failed" in cleaned

def test_batch_clean_length(sample_reviews):
    cleaned_list = [TextPreprocessor.clean_text(r) for r in sample_reviews if r]
    assert len(cleaned_list) == 2  # Filters out empty/None entries