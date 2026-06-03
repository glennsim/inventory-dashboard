"""Flask application factory and route handlers."""

from flask import Flask, render_template, jsonify, request
from modules.excel_reader import ExcelReader
from modules.inventory_manager import InventoryManager
import config

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize managers
    excel_reader = ExcelReader(config.EXCEL_FILE_PATH)
    inventory_manager = InventoryManager(excel_reader)
    
    @app.route('/')
    def index():
        """Render the main dashboard page."""
        return render_template('dashboard.html')
    
    @app.route('/api/inventory')
    def get_inventory():
        """API endpoint to fetch inventory data."""
        try:
            data = inventory_manager.get_inventory()
            return jsonify({
                'status': 'success',
                'data': data,
                'total_items': len(data),
                'timestamp': inventory_manager.get_last_updated()
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/inventory/search')
    def search_inventory():
        """API endpoint to search inventory by item name or SKU."""
        query = request.args.get('q', '').strip()
        try:
            results = inventory_manager.search(query)
            return jsonify({
                'status': 'success',
                'data': results,
                'total_results': len(results)
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/inventory/refresh', methods=['POST'])
    def refresh_inventory():
        """API endpoint to manually refresh inventory data."""
        try:
            inventory_manager.refresh()
            return jsonify({
                'status': 'success',
                'message': 'Inventory refreshed successfully',
                'timestamp': inventory_manager.get_last_updated()
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/inventory/stats')
    def get_stats():
        """API endpoint to get inventory statistics."""
        try:
            stats = inventory_manager.get_stats()
            return jsonify({
                'status': 'success',
                'data': stats
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
    
    return app
