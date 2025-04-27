import os
from flask import Flask, jsonify, request, abort
import logging
import requests
from requests.exceptions import RequestException

# Configuration
class Config:
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    HOST = os.environ.get('HOST', '0.0.0.0')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    ORDERS_SERVICE_URL = os.environ.get('ORDERS_SERVICE_URL', 'http://demo_orders:5000')
    ITEMS_SERVICE_URL = os.environ.get('ITEMS_SERVICE_URL', 'http://demo_items:5000')
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 5))

# Initialize app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = app.logger

@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    logger.info(f'Retrieving detailed order for ID: {order_id}')
    try:
        # Get order details
        order_url = f'{Config.ORDERS_SERVICE_URL}/order/{order_id}'
        logger.debug(f'Requesting order from: {order_url}')
        
        order_response = requests.get(order_url, timeout=Config.REQUEST_TIMEOUT)
        if order_response.status_code != 200:
            logger.warning(f'Order service returned status: {order_response.status_code}')
            abort(order_response.status_code, description='Error retrieving order details')
            
        order = order_response.json()
        
        # Get items for this order
        items = []
        for item_id in order.get('items', []):
            try:
                item = _fetch_item(item_id)
                items.append(item)
            except Exception as e:
                logger.error(f'Error fetching item {item_id}: {str(e)}')
                # Continue with partial data
        
        # Replace item IDs with item details
        del order['items']
        order['items'] = items
        
        return jsonify(order), 200
        
    except RequestException as e:
        logger.error(f'Request error for order {order_id}: {str(e)}')
        abort(503, description='Service unavailable')
    except Exception as e:
        logger.error(f'Error processing order {order_id}: {str(e)}')
        abort(500, description='Internal server error')

def _fetch_item(item_id):
    """Fetch item details from items service"""
    item_url = f'{Config.ITEMS_SERVICE_URL}/item/{item_id}'
    logger.debug(f'Requesting item from: {item_url}')
    
    item_response = requests.get(item_url, timeout=Config.REQUEST_TIMEOUT)
    if item_response.status_code != 200:
        logger.warning(f'Item service returned status: {item_response.status_code} for item {item_id}')
        raise Exception(f'Failed to retrieve item {item_id}')
        
    return item_response.json()

if __name__ == '__main__':
    logger.info(f'Starting aggregate service on {Config.HOST}')
    app.run(debug=Config.DEBUG, host=Config.HOST)
