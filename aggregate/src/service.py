import requests
import logging
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class AggregateService:
    """Service layer for the aggregate service"""
    
    def __init__(self, orders_url, items_url, timeout=5):
        self.orders_url = orders_url
        self.items_url = items_url
        self.timeout = timeout
        logger.info(f"Initialized AggregateService with orders_url={orders_url}, items_url={items_url}")

    def get_order_details(self, order_id):
        """
        Get detailed order information by combining order data with item details
        """
        logger.info(f"Getting detailed information for order {order_id}")
        
        # Get order data
        order = self._get_order(order_id)
        if not order:
            return None
            
        # Get item details
        item_ids = order.get('items', [])
        items = []
        for item_id in item_ids:
            try:
                item = self._get_item(item_id)
                if item:
                    items.append(item)
            except RequestException as e:
                logger.error(f"Request error fetching item {item_id}: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error fetching item {item_id}: {str(e)}")
        
        result = dict(order)
        result['items'] = items
        
        return result
    
    def _get_order(self, order_id):
        """Fetch order data from the orders service"""
        url = f"{self.orders_url}/order/{order_id}"
        logger.debug(f"Requesting order from {url}")
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Request error fetching order {order_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing order {order_id}: {str(e)}")
            raise
    
    def _get_item(self, item_id):
        """Fetch item data from the items service"""
        url = f"{self.items_url}/item/{item_id}"
        logger.debug(f"Requesting item from {url}")
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Request error fetching item {item_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing item {item_id}: {str(e)}")
            raise