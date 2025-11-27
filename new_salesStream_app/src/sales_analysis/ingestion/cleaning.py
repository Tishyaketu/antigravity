def currency_cleaner(value):
    """
    Robustly parses currency strings (e.g., '₹1,099') into floats.
    Handles missing values, currency symbols, and commas.
    """
    if not value or not isinstance(value, str):
        return 0.0
    try:
        # Remove symbol and commas to get raw number string
        return float(value.replace('₹', '').replace(',', '').strip())
    except ValueError:
        return 0.0

def percent_cleaner(value):
    """
    Parses percentage strings (e.g., '64%') into floats.
    """
    if not value or not isinstance(value, str):
        return 0.0
    try:
        return float(value.replace('%', '').strip())
    except ValueError:
        return 0.0

def rating_cleaner(value):
    """
    Parses rating strings which might contain extra metadata (e.g., '4.5|...').
    Extracts the primary numeric rating.
    """
    if not value:
        return 0.0
    try:
        # Split by pipe to handle cases where rating has appended text
        return float(str(value).split('|')[0].strip())
    except (ValueError, AttributeError):
        return 0.0

def count_cleaner(value):
    """
    Parses count strings with commas (e.g., '24,269') into integers.
    """
    if not value: 
        return 0
    try:
        return int(str(value).replace(',', '').strip())
    except ValueError:
        return 0