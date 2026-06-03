"""Script to generate sample inventory data for testing."""

import pandas as pd
from pathlib import Path

def create_sample_inventory():
    """
    Create a sample inventory Excel file.
    """
    # Sample data
    data = {
        'Item': [
            'Widget A',
            'Widget B',
            'Widget C',
            'Gadget X',
            'Gadget Y',
            'Gadget Z',
            'Component P',
            'Component Q',
            'Component R',
            'Assembly 1',
            'Assembly 2',
            'Assembly 3'
        ],
        'SKU': [
            'SKU001',
            'SKU002',
            'SKU003',
            'SKU004',
            'SKU005',
            'SKU006',
            'SKU007',
            'SKU008',
            'SKU009',
            'SKU010',
            'SKU011',
            'SKU012'
        ],
        'Quantity': [
            150,
            75,
            200,
            0,
            45,
            120,
            300,
            25,
            89,
            500,
            10,
            175
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    output_path = Path(__file__).parent / 'inventory.xlsx'
    df.to_excel(output_path, sheet_name='Inventory', index=False)
    
    print(f"Sample inventory created at: {output_path}")
    print(f"Total items: {len(df)}")
    print(f"\n{df}")

if __name__ == '__main__':
    create_sample_inventory()
