"""HTML parsing utilities"""
import logging
from bs4 import BeautifulSoup
from scraper.utils import retry

logger = logging.getLogger(__name__)

class JobParser:
    """Parser for job listings"""
    
    @staticmethod
    @retry(max_attempts=3)
    def parse_job_list(html_content):
        """Parse job list from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            jobs = []
            
            # TODO: Adjust selectors based on actual jobz.az structure
            job_elements = soup.find_all('div', class_='job-item')
            
            for job_elem in job_elements:
                try:
                    job_data = {
                        'title': job_elem.find('h2', class_='job-title').text.strip(),
                        'company': job_elem.find('span', class_='company-name').text.strip(),
                        'description': job_elem.find('p', class_='job-description').text.strip(),
                        'category': job_elem.find('span', class_='category').text.strip(),
                        'city': job_elem.find('span', class_='city').text.strip(),
                        'salary': job_elem.find('span', class_='salary').text.strip() if job_elem.find('span', class_='salary') else None,
                        'job_type': job_elem.find('span', class_='job-type').text.strip() if job_elem.find('span', class_='job-type') else None,
                        'external_url': job_elem.find('a', class_='job-link')['href'] if job_elem.find('a', class_='job-link') else None,
                    }
                    jobs.append(job_data)
                except AttributeError as e:
                    logger.warning(f"Error parsing job element: {e}")
                    continue
            
            return jobs
        except Exception as e:
            logger.error(f"Error parsing job list: {e}")
            raise
    
    @staticmethod
    def extract_salary_range(salary_text):
        """Extract min and max salary from text"""
        try:
            # TODO: Implement salary extraction logic
            return {'min': None, 'max': None}
        except Exception as e:
            logger.error(f"Error extracting salary: {e}")
            return {'min': None, 'max': None}
