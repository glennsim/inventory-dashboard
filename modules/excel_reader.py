"""Module for reading and handling Excel files."""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelReader:
    """Handles reading and parsing Excel files."""
    
    def __init__(self, file_path, sheet_name=0):
        """
        Initialize the Excel reader.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name or index of the sheet to read (default: 0)
        """
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.data = None
        self.last_modified = None
        
    def read(self):
        """
        Read the Excel file and return data as DataFrame.
        
        Returns:
            pandas.DataFrame: Data from the Excel file
            
        Raises:
            FileNotFoundError: If the Excel file doesn't exist
            ValueError: If the file cannot be read
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")
        
        try:
            logger.info(f"Reading Excel file: {self.file_path}")
            self.data = pd.read_excel(
                self.file_path,
                sheet_name=self.sheet_name,
                engine='openpyxl'
            )
            
            # Store modification time
            self.last_modified = self.file_path.stat().st_mtime
            
            logger.info(f"Successfully read {len(self.data)} rows from Excel file")
            return self.data
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise ValueError(f"Cannot read Excel file: {str(e)}")
    
    def get_data(self):
        """
        Get the current data without re-reading.
        
        Returns:
            pandas.DataFrame: Current data or None if not read yet
        """
        return self.data
    
    def validate_columns(self, required_columns):
        """
        Validate that required columns exist in the data.
        
        Args:
            required_columns: List of required column names
            
        Returns:
            bool: True if all required columns exist
            
        Raises:
            ValueError: If any required column is missing
        """
        if self.data is None:
            raise ValueError("No data loaded. Call read() first.")
        
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}. "
                f"Available columns: {', '.join(self.data.columns)}"
            )
        
        return True
    
    def has_changed(self):
        """
        Check if the file has been modified since last read.
        
        Returns:
            bool: True if the file has been modified
        """
        if not self.file_path.exists():
            return False
        
        current_modified = self.file_path.stat().st_mtime
        return self.last_modified != current_modified if self.last_modified else True
