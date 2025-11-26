import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from stream_processor import Stream
from models import Product
from utils import clean_currency, clean_rating, clean_count

class TestStreamProcessor(unittest.TestCase):
    
    def setUp(self):
        """Prepare dummy data for testing."""
        self.raw_data = [
            # Name, Category, DiscPrice, ActPrice, Disc%, Rating, Count
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100),
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100), # Duplicate
            Product("Mouse", "Electronics", 50.0, 100.0, 50.0, 4.0, 50),
            Product("Shirt", "Clothing", 20.0, 40.0, 50.0, 3.5, 10),
            Product("Pen", "Office", 5.0, 5.0, 0.0, 4.8, 500),
        ]
        self.stream = Stream(self.raw_data)

    # --- TEST UTILITIES ---
    def test_clean_currency(self):
        self.assertEqual(clean_currency("₹1,099"), 1099.0)
        self.assertEqual(clean_currency("1,000"), 1000.0)
        self.assertEqual(clean_currency(""), 0.0)
        self.assertEqual(clean_currency(None), 0.0)

    def test_clean_rating(self):
        self.assertEqual(clean_rating("4.5"), 4.5)
        self.assertEqual(clean_rating("4.5|1234"), 4.5)  # Handling dirty separator
        self.assertEqual(clean_rating("NotRated"), 0.0)

    # --- TEST STREAM OPERATIONS ---
    def test_map(self):
        """Test if map can extract prices."""
        prices = self.stream.map(lambda p: p.discounted_price).collect()
        self.assertEqual(prices, [1000.0, 1000.0, 50.0, 20.0, 5.0])

    def test_filter(self):
        """Test if filter keeps only high-rated items."""
        high_rated = self.stream.filter(lambda p: p.rating > 4.2).collect()
        self.assertEqual(len(high_rated), 3)  # Laptop, Laptop, Pen

    def test_distinct(self):
        """Test deduplication."""
        unique_items = self.stream.distinct(lambda p: p.name).collect()
        self.assertEqual(len(unique_items), 4) # Should remove one 'Laptop'
        self.assertEqual(unique_items[0].name, "Laptop")
        self.assertEqual(unique_items[1].name, "Mouse")

    def test_reduce(self):
        """Test summation of revenue."""
        total_rev = self.stream \
            .map(lambda p: p.discounted_price) \
            .reduce(lambda acc, x: acc + x, 0.0)
        self.assertEqual(total_rev, 2075.0)

    def test_sorted(self):
        """Test sorting by price."""
        cheapest_first = self.stream \
            .sorted(key=lambda p: p.discounted_price) \
            .collect()
        self.assertEqual(cheapest_first[0].name, "Pen")     # 5.0
        self.assertEqual(cheapest_first[-1].name, "Laptop") # 1000.0

    def test_group_by(self):
        """Test grouping by category."""
        groups = self.stream.group_by(lambda p: p.category)
        self.assertIn("Electronics", groups)
        self.assertIn("Clothing", groups)
        self.assertEqual(len(groups["Electronics"]), 3) # Laptop + Laptop + Mouse
        self.assertEqual(len(groups["Clothing"]), 1)

    # --- TEST ANALYSIS LOGIC (Simulating Main.py) ---
    def test_analysis_verified_hits(self):
        """
        Simulate the 'Verified Hits' analysis:
        Filter > 4.0 rating AND > 90 reviews.
        """
        hits = self.stream \
            .filter(lambda p: p.rating >= 4.0 and p.rating_count > 90) \
            .distinct(lambda p: p.name) \
            .collect()
        
        # Should match Laptop (4.5, 100) and Pen (4.8, 500)
        self.assertEqual(len(hits), 2)
        names = [p.name for p in hits]
        self.assertIn("Laptop", names)
        self.assertIn("Pen", names)

if __name__ == '__main__':
    unittest.main()