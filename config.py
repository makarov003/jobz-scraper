import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Database
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/jobz_scraper'
    )
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'jobz_scraper')
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    API_DEBUG = os.getenv('API_DEBUG', 'False') == 'True'
    
    # Scraper
    SCRAPER_TIMEOUT = int(os.getenv('SCRAPER_TIMEOUT', 30))
    SCRAPER_RETRY_COUNT = int(os.getenv('SCRAPER_RETRY_COUNT', 3))
    SCRAPER_DELAY = int(os.getenv('SCRAPER_DELAY', 2))
    
    # Selenium
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'True') == 'True'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Target URL
    TARGET_URL = 'https://jobz.az'

class DevelopmentConfig(Config):
    """Development configuration"""
    API_DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    API_DEBUG = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration"""
    DATABASE_URL = 'sqlite:///:memory:'
    API_DEBUG = True

config = DevelopmentConfig()
