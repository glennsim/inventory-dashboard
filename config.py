import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Excel file settings
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', os.path.join(BASE_DIR, 'data', 'inventory.xlsx'))
EXCEL_SHEET_NAME = 'Inventory'  # Change to your sheet name

# Required columns in Excel file
REQUIRED_COLUMNS = ['Item', 'SKU', 'Quantity']

# Flask settings
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)

# Refresh settings (in seconds)
REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', 60))

# Display settings
ITEMS_PER_PAGE = 20
SORTING_COLUMN = 'Item'  # Default sort column
