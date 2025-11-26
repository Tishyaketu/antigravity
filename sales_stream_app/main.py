import sys
import os

# Ensure imports work from the 'src' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from stream_processor import Stream
from data_loader import csv_reader

# Path to the dataset
FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'amazon.csv')

def get_stream():
    """Helper to create a fresh Stream generator from the file."""
    return Stream(csv_reader(FILE_PATH))

def main():
    print("\n" + "="*50)
    print(" AMAZON PRODUCT STREAM ANALYSIS ")
    print("="*50 + "\n")

    # ---------------------------------------------------------
    # ANALYSIS 1: KEY FINANCIAL METRICS
    # Demonstrates: Map, Reduce
    # ---------------------------------------------------------
    print("[1] KEY FINANCIAL METRICS")
    
    # Calculate Total Revenue
    total_revenue = get_stream() \
        .map(lambda p: p.discounted_price) \
        .reduce(lambda acc, price: acc + price, 0.0)

    # Calculate Total Savings (Actual - Discounted)
    total_savings = get_stream() \
        .map(lambda p: p.savings) \
        .reduce(lambda acc, val: acc + val, 0.0)
        
    print(f"   > Total Revenue Generated:     ₹{total_revenue:,.2f}")
    print(f"   > Total Savings for Customers: ₹{total_savings:,.2f}")


    # ---------------------------------------------------------
    # ANALYSIS 2: CATEGORY PERFORMANCE
    # Demonstrates: Group By, Aggregation
    # ---------------------------------------------------------
    print("\n[2] AVERAGE RATING BY CATEGORY")
    
    # Group products by their category
    grouped_data = get_stream().group_by(lambda p: p.category)
    
    category_results = []
    
    for category, products in grouped_data.items():
        if not products: continue
        
        # Calculate Average Rating for this group
        count = len(products)
        avg_rating = sum(p.rating for p in products) / count
        
        # Only show categories with meaningful data
        if count > 0:
            category_results.append((category, avg_rating, count))
    
    # Sort categories by rating (Highest first)
    category_results.sort(key=lambda x: x[1], reverse=True)
    
    for cat, rating, count in category_results:
        print(f"   > {cat:<25} : {rating:.2f} stars ({count} products)")


    # ---------------------------------------------------------
    # ANALYSIS 3: TOP 5 MOST DISCOUNTED PRODUCTS
    # Demonstrates: Filter, Sort, DISTINCT (New!), Map, Slicing
    # ---------------------------------------------------------
    print("\n[3] TOP 5 MOST DISCOUNTED PRODUCTS")
    
    top_discounts = get_stream() \
        .filter(lambda p: p.discount_percentage > 0) \
        .sorted(key=lambda p: p.discount_percentage, reverse=True) \
        .distinct(lambda p: p.name) \
        .map(lambda p: f"{p.discount_percentage}% off: {p.name[:50]}...") \
        .collect()[:5]  # Materialize and slice the top 5
    
    for item in top_discounts:
        print(f"   > {item}")


    # ---------------------------------------------------------
    # ANALYSIS 4: VERIFIED HITS
    # Demonstrates: Complex Logic (High Rating AND High Volume)
    # ---------------------------------------------------------
    print("\n[4] VERIFIED HITS (Rating > 4.5 & Reviews > 1000)")
    
    verified_hits = get_stream() \
        .filter(lambda p: p.rating > 4.5 and p.rating_count > 1000) \
        .sorted(key=lambda p: p.rating_count, reverse=True) \
        .distinct(lambda p: p.name) \
        .collect()[:5]

    if not verified_hits:
        print("   > No products matched criteria (Check CSV parsing)")
    else:
        for p in verified_hits:
            print(f"   > [{p.rating} stars | {p.rating_count} reviews] {p.name[:60]}...")
            
    print("\n" + "="*50)

if __name__ == "__main__":
    main()