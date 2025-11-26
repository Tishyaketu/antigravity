def clean_currency(value):
    """
    Converts currency strings like '₹1,099' or '₹1,099.00' to float 1099.0.
    Handles dirty data like empty strings or 'Not Available'.
    """
    if not value or not isinstance(value, str):
        return 0.0
    try:
        # Remove currency symbol, commas, and whitespace
        cleaned = value.replace('₹', '').replace(',', '').strip()
        return float(cleaned)
    except ValueError:
        return 0.0

def clean_percentage(value):
    """
    Converts percentage strings like '64%' to float 64.0.
    """
    if not value or not isinstance(value, str):
        return 0.0
    try:
        # Remove % symbol
        return float(value.replace('%', '').strip())
    except ValueError:
        return 0.0

def clean_rating(value):
    """
    Parses rating strings. Handles dirty data like '4.5|234' or text errors.
    """
    if not value:
        return 0.0
    try:
        # Some rows might contain delimiters; take the first part
        clean_val = str(value).split('|')[0].strip()
        return float(clean_val)
    except (ValueError, AttributeError):
        return 0.0

def clean_count(value):
    """
    Parses integer counts with commas, e.g., '24,269' -> 24269.
    """
    if not value: 
        return 0
    try:
        # Remove commas
        return int(str(value).replace(',', '').strip())
    except ValueError:
        return 0