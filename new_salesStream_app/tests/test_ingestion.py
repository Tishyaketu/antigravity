import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from sales_analysis.ingestion.cleaning import (
    clean_currency, clean_percentage, clean_rating, clean_count
)
from sales_analysis.ingestion.loader import csv_reader

class TestIngestion(unittest.TestCase):

    # --- Cleaning Tests ---
    def test_clean_currency_edge_cases(self):
        self.assertEqual(clean_currency(None), 0.0)
        self.assertEqual(clean_currency(100), 0.0) # Not a string
        self.assertEqual(clean_currency("invalid"), 0.0)
        self.assertEqual(clean_currency("₹ 1,200.50 "), 1200.50)

    def test_clean_percentage(self):
        self.assertEqual(clean_percentage("50%"), 50.0)
        self.assertEqual(clean_percentage(" 12 % "), 12.0)
        self.assertEqual(clean_percentage(None), 0.0)
        self.assertEqual(clean_percentage("abc"), 0.0)

    def test_clean_count(self):
        self.assertEqual(clean_count("1,000"), 1000)
        self.assertEqual(clean_count("500"), 500)
        self.assertEqual(clean_count(None), 0)
        self.assertEqual(clean_count("abc"), 0)

    def test_clean_rating_edge_cases(self):
        self.assertEqual(clean_rating(None), 0.0)
        self.assertEqual(clean_rating("invalid"), 0.0)
        # Test the split logic
        self.assertEqual(clean_rating("4.5|12345"), 4.5)

    # --- Loader Tests ---
    @patch('os.path.exists')
    def test_loader_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        # Should return empty generator or handle error gracefully
        products = list(csv_reader("non_existent.csv"))
        self.assertEqual(len(products), 0)

    @patch('os.path.exists')
    def test_loader_valid_file(self, mock_exists):
        mock_exists.return_value = True
        
        csv_data = (
            "product_name,category,discounted_price,actual_price,discount_percentage,rating,rating_count\n"
            "Test Product,Electronics|Computers,₹100,₹200,50%,4.5,10"
        )
        
        with patch('builtins.open', mock_open(read_data=csv_data)):
            products = list(csv_reader("dummy.csv"))
            
            self.assertEqual(len(products), 1)
            p = products[0]
            self.assertEqual(p.name, "Test Product")
            self.assertEqual(p.category, "Electronics") # Should split category
            self.assertEqual(p.discounted_price, 100.0)
            self.assertEqual(p.rating, 4.5)
