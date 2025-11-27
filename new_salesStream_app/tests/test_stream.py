import unittest
import sys
import os

# 1. Point to 'src' to find the new package structure
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

# 2. Updated Imports reflecting the new modular structure
from sales_analysis.core.stream import Stream
from sales_analysis.core.models import Product
from sales_analysis.ingestion.cleaning import (
    currency_cleaner, rating_cleaner, count_cleaner
)

class TestStreamProcessor(unittest.TestCase):
    
    def setUp(self):
        """
        Runs before EACH test.
        Creates a fresh dataset so tests don't interfere with each other.
        """
        self.raw_data = [
            # Name, Category, DiscPrice, ActPrice, Disc%, Rating, Count
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100),
            Product("Laptop", "Electronics", 1000.0, 1500.0, 33.0, 4.5, 100), # Duplicate
            Product("Mouse", "Electronics", 50.0, 100.0, 50.0, 4.0, 50),
            Product("Shirt", "Clothing", 20.0, 40.0, 50.0, 3.5, 10),
            Product("Pen", "Office", 5.0, 5.0, 0.0, 4.8, 500),
        ]
        self.stream = Stream(self.raw_data)

    # --- PART 1: TESTING UTILITIES (Ingestion) ---
    
    def test_clean_currency(self):
        """Test if currency strings are parsed correctly."""
        self.assertEqual(currency_cleaner("₹1,099"), 1099.0)
        self.assertEqual(currency_cleaner("1,000"), 1000.0)
        self.assertEqual(currency_cleaner(None), 0.0)

    def test_clean_rating(self):
        """Test if dirty rating strings are fixed."""
        self.assertEqual(rating_cleaner("4.5"), 4.5)
        self.assertEqual(rating_cleaner("4.5|1234"), 4.5)
        self.assertEqual(rating_cleaner("NotRated"), 0.0)

    # --- PART 2: TESTING CORE STREAM LOGIC ---

    def test_map(self):
        """Test if map can transform data (Extract prices)."""
        # Should extract: [1000.0, 1000.0, 50.0, 20.0, 5.0]
        prices = self.stream.map(lambda p: p.discounted_price).collect()
        self.assertEqual(prices[0], 1000.0)
        self.assertEqual(prices[-1], 5.0)

    def test_filter(self):
        """Test if filter keeps only items matching a condition."""
        # Filter: Rating > 4.2 (Laptop, Laptop, Pen)
        high_rated = self.stream.filter(lambda p: p.rating > 4.2).collect()
        self.assertEqual(len(high_rated), 3)
        self.assertEqual(high_rated[2].name, "Pen")

    def test_distinct(self):
        """Test deduplication (Senior Engineer Feature)."""
        # Should remove the second 'Laptop'
        unique_items = self.stream.distinct(lambda p: p.name).collect()
        self.assertEqual(len(unique_items), 4)
        names = [p.name for p in unique_items]
        self.assertEqual(names.count("Laptop"), 1)

    def test_sorted(self):
        """Test sorting logic."""
        # Sort by Price Ascending: Pen (5.0) should be first
        cheapest_first = self.stream \
            .sorted(key=lambda p: p.discounted_price) \
            .collect()
        self.assertEqual(cheapest_first[0].name, "Pen")
        self.assertEqual(cheapest_first[-1].name, "Laptop")

    def test_group_by(self):
        """Test grouping aggregation."""
        groups = self.stream.group_by(lambda p: p.category)
        self.assertIn("Electronics", groups)
        self.assertIn("Clothing", groups)
        # Electronics should have 3 items (Laptop, Laptop, Mouse)
        self.assertEqual(len(groups["Electronics"]), 3)

    def test_reduce(self):
        """Test accumulation (Summing revenue)."""
        total_rev = self.stream \
            .map(lambda p: p.discounted_price) \
            .reduce(lambda acc, x: acc + x, 0.0)
        # 1000 + 1000 + 50 + 20 + 5 = 2075.0
        self.assertEqual(total_rev, 2075.0)

    # --- PART 3: INTEGRATION TEST (The "Whole Chain") ---
    
    def test_complex_chain(self):
        """
        Simulate a real business query: 
        'Find unique Electronics products sorted by price'
        Verifies that multiple stream operations can be chained correctly.
        """
        result = self.stream \
            .filter(lambda p: p.category == "Electronics") \
            .distinct(lambda p: p.name) \
            .sorted(key=lambda p: p.discounted_price) \
            .collect()
        
        # Should result in: [Mouse (50.0), Laptop (1000.0)]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Mouse")
        self.assertEqual(result[1].name, "Laptop")

if __name__ == '__main__':
    unittest.main()