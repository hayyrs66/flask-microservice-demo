import logging
import os
from flask import Flask

def setup_logger(app_name):
    """Set up and configure a logger for the application"""
    logger = logging.getLogger(app_name)
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logger

def create_flask_app(name):
    """Create and configure a Flask application"""
    app = Flask(name)
    # Add any common middleware or configurations here
    return app

class BaseConfig:
    """Base configuration class that can be extended by services"""
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    HOST = os.environ.get('HOST', '0.0.0.0')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 5))

class ServiceURLs:
    """Configuration for service URLs"""
    ORDERS_SERVICE = os.environ.get('ORDERS_SERVICE_URL', 'http://demo_orders:5000')
    ITEMS_SERVICE = os.environ.get('ITEMS_SERVICE_URL', 'http://demo_items:5000')
    AGGREGATE_SERVICE = os.environ.get('AGGREGATE_SERVICE_URL', 'http://demo_aggregate:5000')