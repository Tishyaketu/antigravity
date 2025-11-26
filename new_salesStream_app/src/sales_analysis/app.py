from sales_analysis.core.stream import Stream
from sales_analysis.ingestion.loader import csv_reader

def get_stream(file_path):
    """
    Factory function to create a new Stream instance.
    Crucial: Since generators are single-use, we must create a NEW stream/generator
    for each distinct analysis pipeline (Metrics, Categories, Top Discounts, etc.).
    """
    return Stream(csv_reader(file_path))

def main(file_path):
    print("\n" + "="*50)
    print(" AMAZON PRODUCT STREAM ANALYSIS ")
    print("="*50)

    # [1] KEY METRICS
    # Calculate global financial totals using map-reduce.
    # Note: We re-create the stream for each calculation because the previous stream is consumed.
    print("\n[1] KEY FINANCIAL METRICS")
    total_revenue = get_stream(file_path) \
        .map(lambda p: p.discounted_price) \
        .reduce(lambda acc, x: acc + x, 0.0)
    
    total_savings = get_stream(file_path) \
        .map(lambda p: p.savings) \
        .reduce(lambda acc, x: acc + x, 0.0)

    print(f"   > Total Revenue:     ₹{total_revenue:,.2f}")
    print(f"   > Customer Savings:  ₹{total_savings:,.2f}")

    # [2] CATEGORY ANALYSIS
    # Group products by category to compute aggregate statistics (average rating).
    print("\n[2] AVERAGE RATING BY CATEGORY")
    grouped = get_stream(file_path).group_by(lambda p: p.category)
    
    cat_stats = []
    for cat, products in grouped.items():
        if not products: continue
        # Compute average rating for the category
        avg = sum(p.rating for p in products) / len(products)
        cat_stats.append((cat, avg, len(products)))
    
    # Sort categories by average rating (descending) for display
    for cat, avg, count in sorted(cat_stats, key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   > {cat:<25} : {avg:.2f} stars ({count} items)")

    # [3] TOP DISCOUNTS (Unique)
    # Filter for discounted items, sort by percentage, and deduplicate by name.
    # This pipeline demonstrates chaining filter -> sorted -> distinct.
    print("\n[3] TOP 5 MOST DISCOUNTED PRODUCTS")
    top_discounts = get_stream(file_path) \
        .filter(lambda p: p.discount_percentage > 0) \
        .sorted(key=lambda p: p.discount_percentage, reverse=True) \
        .distinct(lambda p: p.name) \
        .collect()[:5]

    for p in top_discounts:
        print(f"   > {p.discount_percentage}% off: {p.name[:50]}...")

    # [4] VERIFIED HITS
    # Find high-quality products (high rating + high review count).
    print("\n[4] VERIFIED HITS (>4.5 Stars, >1000 Reviews)")
    hits = get_stream(file_path) \
        .filter(lambda p: p.rating > 4.5 and p.rating_count > 1000) \
        .sorted(key=lambda p: p.rating_count, reverse=True) \
        .distinct(lambda p: p.name) \
        .collect()[:5]

    for p in hits:
        print(f"   > [{p.rating}★ | {p.rating_count} reviews] {p.name[:60]}...")
    
    print("\n" + "="*50)