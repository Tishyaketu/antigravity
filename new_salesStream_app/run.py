import sys
import os

# Add 'src' to the python path so we can import the 'sales_analysis' package
# This dynamic path manipulation allows running the script from the root directory
# without setting PYTHONPATH manually.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sales_analysis.app import main

if __name__ == "__main__":
    # Define the absolute path to the dataset
    # Uses __file__ to locate the data directory relative to this script
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'amazon.csv')
    
    # Trigger the application
    main(DATA_PATH)