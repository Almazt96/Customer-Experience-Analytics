# test_scraperandpreprocessing.py
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys

# 1. Prevent real database connections during testing by pre-mocking imports
sys.modules['psycopg2'] = MagicMock()
sys.modules['sqlalchemy'] = MagicMock()

# 2. Safely import your function now that the database calls are neutralized
from scraperandpreprocessing import scrape_bank_reviews

class TestBankScraper(unittest.TestCase):

    def setUp(self):
        """Set up standard sample data format returned by google_play_scraper."""
        self.mock_reviews_data = [
            {
                'reviewId': '123',
                'userName': 'User One',
                'content': 'Great banking app!',
                'score': 5,
                'thumbsUpCount': 2,
                'at': '2026-05-15 10:00:00'
            },
            {
                'reviewId': '456',
                'userName': 'User Two',
                'content': 'Slow loading times.',
                'score': 2,
                'thumbsUpCount': 0,
                'at': '2026-05-15 11:00:00'
            }
        ]

    @patch('scraperandpreprocessing.reviews')
    def test_scrape_bank_reviews_success(self, mock_reviews_func):
        """Test that scrape_bank_reviews cleanly builds a DataFrame with proper bank tags."""
        # Configure the mock to return data like the real web API
        mock_reviews_func.return_value = (self.mock_reviews_data, None)

        # Execute
        df = scrape_bank_reviews('com.combanketh.mobilebanking', 'CBE')

        # Assertions
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn('bank', df.columns)
        self.assertEqual(df['bank'].iloc[0], 'CBE')
        self.assertEqual(df['content'].iloc[0], 'Great banking app!')

    @patch('scraperandpreprocessing.reviews')
    def test_scrape_bank_reviews_empty(self, mock_reviews_func):
        """Test behavior when an app target returns zero results."""
        mock_reviews_func.return_value = ([], None)

        df = scrape_bank_reviews('com.boa.boaMobileBanking', 'BOA')

        self.assertTrue(df.empty)
        self.assertEqual(len(df), 0)

if __name__ == '__main__':
    unittest.main()