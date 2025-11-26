def clean_currency(value):
    """Parses '₹1,099' -> 1099.0"""
    if not value or not isinstance(value, str):
        return 0.0
    try:
        return float(value.replace('₹', '').replace(',', '').strip())
    except ValueError:
        return 0.0

def clean_percentage(value):
    """Parses '64%' -> 64.0"""
    if not value or not isinstance(value, str):
        return 0.0
    try:
        return float(value.replace('%', '').strip())
    except ValueError:
        return 0.0

def clean_rating(value):
    """Parses '4.5|...' -> 4.5"""
    if not value:
        return 0.0
    try:
        return float(str(value).split('|')[0].strip())
    except (ValueError, AttributeError):
        return 0.0

def clean_count(value):
    """Parses '24,269' -> 24269"""
    if not value: 
        return 0
    try:
        return int(str(value).replace(',', '').strip())
    except ValueError:
        return 0