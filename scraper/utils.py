"""Utility functions for scraper"""
import logging
import time
from functools import wraps
from config import config

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def retry(max_attempts=None, delay=1, backoff=2):
    """Retry decorator"""
    if max_attempts is None:
        max_attempts = config.SCRAPER_RETRY_COUNT
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def rate_limit(delay=None):
    """Rate limiting decorator"""
    if delay is None:
        delay = config.SCRAPER_DELAY
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(delay)
            return result
        return wrapper
    return decorator
