import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from sales_analysis.core.models import Product

class TestModels(unittest.TestCase):
    def test_product_savings(self):
        """
        Verifies that the calculated property 'savings' correctly computes
        the difference between actual and discounted price.
        """
        p = Product(
            name="Test", category="Test", 
            discounted_price=80.0, actual_price=100.0, 
            discount_percentage=20.0, rating=5.0, rating_count=1
        )
        # Explicitly access the property to ensure coverage
        self.assertEqual(p.savings, 20.0)
