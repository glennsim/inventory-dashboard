#!/usr/bin/env python
"""Entry point for the Inventory Dashboard application."""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app
import config

def main():
    """Initialize and run the Flask application."""
    app = create_app()
    
    print(f"\n{'='*60}")
    print("Inventory Dashboard")
    print(f"{'='*60}")
    print(f"Starting server at http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"Excel file: {config.EXCEL_FILE_PATH}")
    print(f"Press CTRL+C to stop")
    print(f"{'='*60}\n")
    
    try:
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
