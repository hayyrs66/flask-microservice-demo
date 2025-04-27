import os
import sys
import logging
from flask import Flask, jsonify, abort
from service import ItemsService

# Add common package to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
try:
    from common.utils import BaseConfig, setup_logger, create_flask_app
except ImportError:
    print("Could not import common utils, using local implementation")
    # Fallback to local implementation if common package isn't available

# Configuration
class Config(BaseConfig):
    ITEM_COUNT = int(os.environ.get('ITEM_COUNT', 100))

# Initialize app
app = create_flask_app(__name__)
logger = setup_logger('items_service')

# Initialize service
items_service = ItemsService(item_count=Config.ITEM_COUNT)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'items',
        'item_count': len(items_service.items)
    }), 200

@app.route('/allItems', methods=['GET'])
def all_items():
    """Get all items"""
    return jsonify(items_service.get_all_items()), 200

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    try:
        item = items_service.get_item_by_id(item_id)
        if item is None:
            abort(404, description=f'Item with ID {item_id} not found')
        return jsonify(item), 200
    except Exception as e:
        logger.error(f'Error retrieving item {item_id}: {str(e)}')
        abort(500, description='Internal server error')

if __name__ == '__main__':
    logger.info(f'Starting items service on {Config.HOST}')
    app.run(debug=Config.DEBUG, host=Config.HOST)
