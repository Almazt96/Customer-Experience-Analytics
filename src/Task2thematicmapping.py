import numpy as np
import pandas as pd

def extract_banking_themes(df: pd.DataFrame, text_column: str = 'review_text') -> pd.DataFrame:
    """
    Categorizes reviews into distinct, bank-relevant themes based on keyword matching
    derived from top TF-IDF features.
    """
    # Define the domain-specific banking themes mapping
    THEME_MATRIX = {
        'Digital Banking & App': [
            'app', 'login', 'crash', 'ui', 'mobile', 'update', 'transfer', 'password', 'biometric', 'error'
        ],
        'Customer Service & Support': [
            'staff', 'wait', 'helpful', 'manager', 'support', 'call', 'branch', 'teller', 'rude', 'line'
        ],
        'Fees & Financial Charges': [
            'interest', 'fee', 'charge', 'hidden', 'overdraft', 'rates', 'annual', 'billing', 'penalty'
        ],
        'Account & Transaction Security': [
            'fraud', 'locked', 'scam', 'security', 'otp', 'verification', 'frozen', 'unauthorized', 'hack'
        ]
    }
    
    theme_labels = []
    
    for text in df[text_column]:
        if not isinstance(text, str):
            theme_labels.append('Uncategorized')
            continue
            
        text_lower = text.lower()
        matched_themes = []
        
        # Check text against the theme matrix
        for theme, keywords in THEME_MATRIX.items():
            if any(keyword in text_lower for keyword in keywords):
                matched_themes.append(theme)
        
        # Assign the primary theme (or flag if multiple/none match)
        if not matched_themes:
            theme_labels.append('General/Other')
        elif len(matched_themes) == 1:
            theme_labels.append(matched_themes[0])
        else:
            # Multi-theme review (could also just return matched_themes as a list)
            theme_labels.append('Multi-Theme')
            
    df['assigned_theme'] = theme_labels
    return df