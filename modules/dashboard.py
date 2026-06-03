"""Utility functions for the dashboard."""

def format_inventory_for_display(items):
    """
    Format inventory items for display.
    
    Args:
        items: List of inventory item dictionaries
        
    Returns:
        list: Formatted items
    """
    formatted = []
    for i, item in enumerate(items, 1):
        formatted.append({
            'id': i,
            'Item': item.get('Item', 'N/A'),
            'SKU': item.get('SKU', 'N/A'),
            'Quantity': item.get('Quantity', 0),
            'Status': get_stock_status(item.get('Quantity', 0))
        })
    return formatted

def get_stock_status(quantity):
    """
    Get the stock status based on quantity.
    
    Args:
        quantity: Current quantity
        
    Returns:
        str: Status label
    """
    if quantity == 0:
        return 'Out of Stock'
    elif quantity < 50:
        return 'Low Stock'
    elif quantity < 100:
        return 'Medium Stock'
    else:
        return 'Good Stock'

def get_status_color(quantity):
    """
    Get the color code for status indicator.
    
    Args:
        quantity: Current quantity
        
    Returns:
        str: CSS color class
    """
    if quantity == 0:
        return 'status-critical'
    elif quantity < 50:
        return 'status-warning'
    elif quantity < 100:
        return 'status-medium'
    else:
        return 'status-good'
