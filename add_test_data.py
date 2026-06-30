import sys
sys.path.insert(0, '.')

from scraper.database import get_session, Job, init_db
from datetime import datetime

init_db()
session = get_session()

# Test məlumatlar
test_jobs = [
    Job(title="Python Developer", company="TechCorp", city="Baku", salary="1500-2500", job_type="Full-time", description="Senior Python developer wanted"),
    Job(title="Frontend Developer", company="WebStudio", city="Ganja", salary="1200-2000", job_type="Full-time", description="React specialist needed"),
    Job(title="Data Analyst", company="DataCo", city="Baku", salary="1800-2800", job_type="Remote", description="Analyze big data"),
    Job(title="DevOps Engineer", company="CloudTech", city="Baku", salary="2000-3000", job_type="Full-time", description="Infrastructure management"),
]

for job in test_jobs:
    session.add(job)

session.commit()
print("✅ Test data əlavə olundu!")
session.close()