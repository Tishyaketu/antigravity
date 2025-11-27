from sales_analysis.core.stream import Stream
from sales_analysis.ingestion.loader import read_csv

def use_stream(file_path):
    """
    Factory function to create a new Stream instance.
    Crucial: Since generators are single-use, we must create a NEW stream/generator
    for each distinct analysis pipeline (Metrics, Categories, Top Discounts, etc.).
    """
    return Stream(read_csv(file_path))

def main(file_path):
    print("\n" + "-"*50)
    print(" AMAZON PRODUCT STREAM ANALYSIS ")
    print("-"*50)

    # [1] KEY METRICS
    # Calculate global financial totals using map-reduce.
    # Note: We re-create the stream for each calculation because the previous stream is consumed.
    print("\n[1] KEY FINANCIAL METRICS")
    cumulative_revenue = use_stream(file_path) \
        .map(lambda product: product.discounted_price) \
        .reduce(lambda acc, x: acc + x, 0.0)
    
    cumulative_savings = use_stream(file_path) \
        .map(lambda product: product.savings) \
        .reduce(lambda acc, x: acc + x, 0.0)

    print(f"   > Total Revenue:     ₹{cumulative_revenue:,.2f}")
    print(f"   > Total Customer Savings:  ₹{cumulative_savings:,.2f}")

    # [2] CATEGORY ANALYSIS
    # Group products by category to compute aggregate statistics (average rating).
    print("\n[2] AVERAGE/MEAN RATING BY CATEGORY")
    grouping = use_stream(file_path).group_by(lambda product: product.category)
    
    category_stats = []
    for cat, products in grouping.items():
        if not products: continue
        # Compute average rating for the category
        avg = sum(product.rating for product in products) / len(products)
        category_stats.append((cat, avg, len(products)))
    
    # Sort categories by average rating (descending) for display
    for cat, avg, count in sorted(category_stats, key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   > {cat:<25} : {avg:.2f} stars ({count} items)")

    # [3] TOP DISCOUNTS (Unique)
    # Filter for discounted items, sort by percentage, and deduplicate by name.
    # This pipeline demonstrates chaining filter -> sorted -> distinct.
    print("\n[3] TOP 5 MOST DISCOUNTED PRODUCTS")
    top_discounts = use_stream(file_path) \
        .filter(lambda product: product.discount_percentage > 0) \
        .sorted(key=lambda product: product.discount_percentage, reverse=True) \
        .distinct(lambda product: product.name) \
        .collect()[:5]

    for product in top_discounts:
        print(f"   > {product.discount_percentage}% off: {product.name[:50]}...")

    # [4] VERIFIED HITS
    # Find high-quality products (high rating + high review count).
    print("\n[4] VERIFIED HITS (>4.5 Stars, >1000 Reviews)")
    verfied_hits = use_stream(file_path) \
        .filter(lambda product: product.rating > 4.5 and product.rating_count > 1000) \
        .sorted(key=lambda product: product.rating_count, reverse=True) \
        .distinct(lambda product: product.name) \
        .collect()[:5]

    for product in verfied_hits:
        print(f"   > [{product.rating}★ | {product.rating_count} reviews] {product.name[:60]}...")
    
    print("\n" + "-"*50)