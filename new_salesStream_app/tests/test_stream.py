import unittest
import sys
import os

# Point to 'src' to find the new package structure
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

# Updated Imports
from sales_analysis.core.stream import Stream
from sales_analysis.core.models import Product
from sales_analysis.ingestion.cleaning import clean_currency

class TestStreamProcessor(unittest.TestCase):
    
    def setUp(self):
        self.raw_data = [
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100),
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100), # Duplicate
            Product("Mouse", "Electronics", 50.0, 100.0, 50.0, 4.0, 50),
        ]
        self.stream = Stream(self.raw_data)

    def test_cleaning(self):
        self.assertEqual(clean_currency("₹1,099"), 1099.0)

    def test_distinct(self):
        """Test deduplication logic"""
        unique = self.stream.distinct(lambda p: p.name).collect()
        self.assertEqual(len(unique), 2) # 1 Laptop, 1 Mouse
        self.assertEqual(unique[0].name, "Laptop")

    def test_logic_chain(self):
        """Test the full chain: Filter -> Sort -> Map"""
        result = self.stream \
            .filter(lambda p: p.category == "Electronics") \
            .distinct(lambda p: p.name) \
            .sorted(key=lambda p: p.discounted_price) \
            .map(lambda p: p.name) \
            .collect()
        
        # Mouse (50.0) should be first, then Laptop (1000.0)
        self.assertEqual(result, ["Mouse", "Laptop"])

if __name__ == '__main__':
    unittest.main()