import csv
import os
from sales_analysis.core.models import Product
from sales_analysis.ingestion.cleaning import (
    currency_cleaner, percent_cleaner, rating_cleaner, count_cleaner
)

def read_csv(file_path):
    """
    A generator function that reads a CSV file row by row.
    Yields Product objects one at a time to avoid loading the entire file into RAM.
    """
    if not os.path.exists(file_path):
        print(f"CRITICAL ERROR: Data file not found at: {file_path}")
        return

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Construct a Product object, applying cleaning functions to raw string data
            yield Product(
                name=row.get('product_name', 'Unknown'),
                category=row.get('category', 'Others').split('|')[0], # Take primary category only
                discounted_price=currency_cleaner(row.get('discounted_price')),
                actual_price=currency_cleaner(row.get('actual_price')),
                discount_percentage=percent_cleaner(row.get('discount_percentage')),
                rating=rating_cleaner(row.get('rating')),
                rating_count=count_cleaner(row.get('rating_count'))
            )