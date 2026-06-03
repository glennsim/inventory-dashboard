# Inventory Dashboard

A flexible Python-based inventory tracking dashboard that pulls data from Excel sheets.

## Features

- **Excel Integration**: Load inventory data directly from Excel files
- **Stock Level Tracking**: Monitor real-time stock levels for all items
- **Web Dashboard**: Interactive web interface for viewing inventory
- **Data Refresh**: Automatic and manual refresh of inventory data
- **Flexible**: Easy to adapt to different data structures

## Project Structure

```
inventory-dashboard/
├── README.md
├── requirements.txt
├── config.py                 # Configuration settings
├── main.py                   # Entry point
├── app.py                    # Flask application
├── data/
│   ├── inventory.xlsx       # Sample Excel file
│   └── sample_data.py       # Sample data generator
├── modules/
│   ├── __init__.py
│   ├── excel_reader.py      # Excel file handler
│   ├── inventory_manager.py # Inventory logic
│   └── dashboard.py         # Dashboard utilities
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── inventory_table.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/glennsim/inventory-dashboard.git
cd inventory-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your Excel file with columns: `Item`, `SKU`, `Quantity`

2. Run the application:
```bash
python main.py
```

3. Open your browser to `http://localhost:5000`

## Excel File Format

Your Excel file should have the following structure:

| Item | SKU | Quantity |
|------|-----|----------|
| Widget A | SKU001 | 150 |
| Widget B | SKU002 | 75 |
| Gadget X | SKU003 | 200 |

## Configuration

Edit `config.py` to customize:
- Excel file path
- Refresh interval
- Port and host settings

## License

MIT
