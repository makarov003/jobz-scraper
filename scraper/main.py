"""Main scraper module"""
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from config import config
from scraper.database import init_db, get_session, Job
from scraper.parser import JobParser
from scraper.utils import setup_logging, retry, rate_limit

logger = logging.getLogger(__name__)
setup_logging()

class JobzScraper:
    """Main scraper class for jobz.az"""
    
    def __init__(self):
        self.base_url = config.TARGET_URL
        self.driver = None
        self.session = None
    
    def setup_selenium(self):
        """Setup Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            if config.HEADLESS_MODE:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(
                executable_path=config.CHROME_DRIVER_PATH,
                options=options
            )
            logger.info("Selenium WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to setup Selenium: {e}")
            raise
    
    def close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium WebDriver closed")
    
    @retry(max_attempts=3)
    @rate_limit()
    def fetch_page(self, url):
        """Fetch page content"""
        try:
            logger.info(f"Fetching: {url}")
            response = requests.get(url, timeout=config.SCRAPER_TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise
    
    def scrape_jobs(self, page=1):
        """Scrape jobs from jobz.az"""
        try:
            logger.info(f"Scraping jobs from page {page}")
            
            # Construct URL with pagination
            url = f"{self.base_url}/jobs?page={page}"
            
            # Fetch page content
            html_content = self.fetch_page(url)
            
            # Parse jobs
            jobs = JobParser.parse_job_list(html_content)
            logger.info(f"Found {len(jobs)} jobs on page {page}")
            
            return jobs
        except Exception as e:
            logger.error(f"Error scraping jobs: {e}")
            raise
    
    def save_jobs(self, jobs):
        """Save jobs to database"""
        try:
            self.session = get_session()
            saved_count = 0
            
            for job_data in jobs:
                try:
                    # Check if job already exists
                    existing_job = self.session.query(Job).filter_by(
                        external_url=job_data.get('external_url')
                    ).first()
                    
                    if existing_job:
                        logger.debug(f"Job already exists: {job_data['title']}")
                        continue
                    
                    # Create new job
                    job = Job(
                        title=job_data.get('title'),
                        company=job_data.get('company'),
                        description=job_data.get('description'),
                        category=job_data.get('category'),
                        city=job_data.get('city'),
                        salary=job_data.get('salary'),
                        job_type=job_data.get('job_type'),
                        external_url=job_data.get('external_url'),
                        posted_date=datetime.utcnow()
                    )
                    
                    self.session.add(job)
                    saved_count += 1
                except Exception as e:
                    logger.warning(f"Error saving job: {e}")
                    continue
            
            self.session.commit()
            logger.info(f"Saved {saved_count} new jobs to database")
            return saved_count
        except Exception as e:
            logger.error(f"Error saving jobs: {e}")
            if self.session:
                self.session.rollback()
            raise
        finally:
            if self.session:
                self.session.close()
    
    def run(self, max_pages=5):
        """Run scraper"""
        try:
            logger.info("Starting jobz.az scraper")
            init_db()
            
            total_jobs = 0
            for page in range(1, max_pages + 1):
                try:
                    jobs = self.scrape_jobs(page=page)
                    if not jobs:
                        logger.info(f"No jobs found on page {page}. Stopping.")
                        break
                    
                    saved = self.save_jobs(jobs)
                    total_jobs += saved
                except Exception as e:
                    logger.error(f"Error processing page {page}: {e}")
                    continue
            
            logger.info(f"Scraping completed. Total new jobs saved: {total_jobs}")
            return total_jobs
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            raise

if __name__ == "__main__":
    scraper = JobzScraper()
    try:
        scraper.run(max_pages=5)
    finally:
        scraper.close_selenium()
