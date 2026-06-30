"""Database operations and models"""
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)
Base = declarative_base()

class Job(Base):
    """Job model"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    salary = Column(String(100), nullable=True)
    job_type = Column(String(50), nullable=True)  # Full-time, Part-time, Freelance
    posted_date = Column(DateTime, nullable=True)
    external_id = Column(String(255), unique=True, nullable=True)
    external_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"

def init_db():
    """Initialize database"""
    try:
        engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
        return engine
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def get_session():
    """Get database session"""
    engine = create_engine(config.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    init_db()
