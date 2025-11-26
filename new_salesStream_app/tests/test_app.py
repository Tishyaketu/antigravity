import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from sales_analysis.app import main
from sales_analysis.core.models import Product

class TestApp(unittest.TestCase):
    
    @patch('sales_analysis.app.csv_reader')
    def test_main_application_flow(self, mock_reader):
        # Mock the data source so we don't need a real file
        mock_data = [
            Product("P1", "Cat1", 100.0, 200.0, 50.0, 4.8, 1500),
            Product("P2", "Cat1", 50.0, 50.0, 0.0, 3.5, 10),
            Product("P3", "Cat2", 20.0, 40.0, 50.0, 4.9, 2000),
        ]
        # Use side_effect to return a FRESH iterator every time it's called
        mock_reader.side_effect = lambda _: iter(mock_data)

        # Capture stdout to verify output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            main("dummy_path.csv")
        finally:
            sys.stdout = sys.__stdout__ # Reset stdout

        output = captured_output.getvalue()
        
        # Verify key parts of the report were printed
        self.assertIn("AMAZON PRODUCT STREAM ANALYSIS", output)
        self.assertIn("Total Revenue:", output)
        self.assertIn("Cat1", output)
        self.assertIn("Cat2", output)
        self.assertIn("VERIFIED HITS", output)
