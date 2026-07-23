# Cleans text & extracts spaCy/TF-IDF themes
import re
from typing import List, Optional

class TextPreprocessor:
    """Preprocesses raw review text for NLP tasks."""
    
    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """Removes special characters, URLs, and extra whitespaces."""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove non-alphanumeric characters while retaining basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?]', '', text)
        # Remove duplicate spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def batch_clean(self, reviews: List[str]) -> List[str]:
        return [self.clean_text(r) for r in reviews if r]