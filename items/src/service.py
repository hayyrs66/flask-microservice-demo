from faker import Faker
import logging

logger = logging.getLogger(__name__)

class ItemsService:
    """Service layer for items management"""
    
    def __init__(self, item_count=100):
        self.fake = Faker()
        self.item_count = item_count
        self.items = self._create_items()
        logger.info(f"Initialized ItemsService with {len(self.items)} items")
    
    def _create_items(self):
        """Create a list of fake items"""
        return [self._create_item(num) for num in range(1, self.item_count + 1)]
    
    def _create_item(self, item_id):
        """Create a single fake item"""
        return {
            'id': item_id,
            'desc': self.fake.bs()
        }
    
    def get_all_items(self):
        """Get all available items"""
        logger.info("Retrieving all items")
        return self.items
    
    def get_item_by_id(self, item_id):
        """Get a specific item by ID"""
        logger.info(f"Retrieving item with ID: {item_id}")
        if item_id < 0 or item_id >= len(self.items):
            logger.warning(f"Item ID {item_id} out of range")
            return None
        return self.items[item_id]