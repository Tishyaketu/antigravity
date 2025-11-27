import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from sales_analysis.ingestion.cleaning import (
    currency_cleaner, percent_cleaner, rating_cleaner, count_cleaner
)
from sales_analysis.ingestion.loader import read_csv

class TestIngestion(unittest.TestCase):

    # --- Cleaning Tests ---
    def test_clean_currency_edge_cases(self):
        """Verify currency cleaner handles None, non-strings, and valid formats."""
        self.assertEqual(currency_cleaner(None), 0.0)
        self.assertEqual(currency_cleaner(100), 0.0) # Not a string
        self.assertEqual(currency_cleaner("invalid"), 0.0)
        self.assertEqual(currency_cleaner("₹ 1,200.50 "), 1200.50)

    def test_clean_percentage(self):
        """Verify percentage cleaner handles symbols and whitespace."""
        self.assertEqual(percent_cleaner("50%"), 50.0)
        self.assertEqual(percent_cleaner(" 12 % "), 12.0)
        self.assertEqual(percent_cleaner(None), 0.0)
        self.assertEqual(percent_cleaner("abc"), 0.0)

    def test_clean_count(self):
        """Verify count cleaner handles commas and invalid inputs."""
        self.assertEqual(count_cleaner("1,000"), 1000)
        self.assertEqual(count_cleaner("500"), 500)
        self.assertEqual(count_cleaner(None), 0)
        self.assertEqual(count_cleaner("abc"), 0)

    def test_clean_rating_edge_cases(self):
        """Verify rating cleaner handles pipe-separated metadata."""
        self.assertEqual(rating_cleaner(None), 0.0)
        self.assertEqual(rating_cleaner("invalid"), 0.0)
        # Test the split logic
        self.assertEqual(rating_cleaner("4.5|12345"), 4.5)

    # --- Loader Tests ---
    @patch('os.path.exists')
    def test_loader_file_not_found(self, mock_exists):
        """Ensure loader handles missing files gracefully (returns empty)."""
        mock_exists.return_value = False
        # Should return empty generator or handle error gracefully
        products = list(read_csv("non_existent.csv"))
        self.assertEqual(len(products), 0)

    @patch('os.path.exists')
    def test_loader_valid_file(self, mock_exists):
        """
        Test successful CSV loading using a mocked file system.
        We use 'mock_open' to simulate reading a file without needing a real one on disk.
        """
        mock_exists.return_value = True
        
        csv_data = (
            "product_name,category,discounted_price,actual_price,discount_percentage,rating,rating_count\n"
            "Test Product,Electronics|Computers,₹100,₹200,50%,4.5,10"
        )
        
        with patch('builtins.open', mock_open(read_data=csv_data)):
            products = list(read_csv("dummy.csv"))
            
            self.assertEqual(len(products), 1)
            p = products[0]
            self.assertEqual(p.name, "Test Product")
            self.assertEqual(p.category, "Electronics") # Should split category
            self.assertEqual(p.discounted_price, 100.0)
            self.assertEqual(p.rating, 4.5)
