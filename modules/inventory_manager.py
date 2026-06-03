"""Module for managing inventory data and operations."""

import logging
from datetime import datetime
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventoryManager:
    """Manages inventory data and operations."""
    
    def __init__(self, excel_reader):
        """
        Initialize the inventory manager.
        
        Args:
            excel_reader: An instance of ExcelReader
        """
        self.excel_reader = excel_reader
        self.inventory_data = None
        self.last_updated = None
        self._load_inventory()
    
    def _load_inventory(self):
        """
        Load inventory data from Excel file.
        """
        try:
            df = self.excel_reader.read()
            self.excel_reader.validate_columns(config.REQUIRED_COLUMNS)
            self.inventory_data = df
            self.last_updated = datetime.now().isoformat()
            logger.info("Inventory loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load inventory: {str(e)}")
            raise
    
    def get_inventory(self):
        """
        Get all inventory items.
        
        Returns:
            list: List of dictionaries containing inventory items
        """
        if self.inventory_data is None:
            return []
        
        # Convert DataFrame to list of dictionaries
        items = self.inventory_data.to_dict('records')
        
        # Clean up and format data
        for item in items:
            # Ensure Quantity is numeric
            try:
                item['Quantity'] = int(item.get('Quantity', 0))
            except (ValueError, TypeError):
                item['Quantity'] = 0
        
        return items
    
    def search(self, query):
        """
        Search inventory by item name or SKU.
        
        Args:
            query: Search query string
            
        Returns:
            list: Filtered list of inventory items
        """
        if not query or self.inventory_data is None:
            return []
        
        query_lower = query.lower()
        
        # Search in Item and SKU columns
        mask = (
            self.inventory_data['Item'].astype(str).str.lower().str.contains(query_lower, na=False) |
            self.inventory_data['SKU'].astype(str).str.lower().str.contains(query_lower, na=False)
        )
        
        results = self.inventory_data[mask].to_dict('records')
        
        # Clean up and format data
        for item in results:
            try:
                item['Quantity'] = int(item.get('Quantity', 0))
            except (ValueError, TypeError):
                item['Quantity'] = 0
        
        return results
    
    def refresh(self):
        """
        Refresh inventory data from Excel file.
        """
        try:
            logger.info("Refreshing inventory data...")
            self._load_inventory()
            logger.info("Inventory refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh inventory: {str(e)}")
            raise
    
    def get_stats(self):
        """
        Get inventory statistics.
        
        Returns:
            dict: Statistics about the inventory
        """
        if self.inventory_data is None:
            return {}
        
        items = self.get_inventory()
        
        total_items = len(items)
        total_quantity = sum(item['Quantity'] for item in items)
        avg_quantity = total_quantity / total_items if total_items > 0 else 0
        
        quantities = [item['Quantity'] for item in items]
        min_quantity = min(quantities) if quantities else 0
        max_quantity = max(quantities) if quantities else 0
        
        low_stock = sum(1 for q in quantities if q < 50)  # Threshold: 50 units
        out_of_stock = sum(1 for q in quantities if q == 0)
        
        return {
            'total_items': total_items,
            'total_quantity': int(total_quantity),
            'average_quantity': round(avg_quantity, 2),
            'min_quantity': int(min_quantity),
            'max_quantity': int(max_quantity),
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock
        }
    
    def get_last_updated(self):
        """
        Get the timestamp of the last update.
        
        Returns:
            str: ISO format timestamp
        """
        return self.last_updated
