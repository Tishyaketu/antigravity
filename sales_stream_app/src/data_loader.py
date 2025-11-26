import csv
from models import Product
from utils import clean_currency, clean_percentage, clean_rating, clean_count

def csv_reader(file_path):
    """
    Generator function acting as an adapter between raw CSV file and Product objects.
    Yields: Product objects (immutable).
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # We perform ETL (Extract, Transform, Load) logic here.
                # Raw strings are cleaned and converted immediately.
                yield Product(
                    name=row.get('product_name', 'Unknown'),
                    # Categories often look like "Electronics|Cables|..." -> We take "Electronics"
                    category=row.get('category', 'Others').split('|')[0],
                    discounted_price=clean_currency(row.get('discounted_price')),
                    actual_price=clean_currency(row.get('actual_price')),
                    discount_percentage=clean_percentage(row.get('discount_percentage')),
                    rating=clean_rating(row.get('rating')),
                    rating_count=clean_count(row.get('rating_count'))
                )
                
    except FileNotFoundError:
        print(f"CRITICAL ERROR: The file {file_path} was not found.")
        return