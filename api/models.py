"""Pydantic models for API"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobBase(BaseModel):
    """Base job model"""
    title: str
    company: str
    description: Optional[str] = None
    category: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None
    external_url: Optional[str] = None

class JobCreate(JobBase):
    """Create job model"""
    pass

class JobResponse(JobBase):
    """Job response model"""
    id: int
    posted_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    """Job list response"""
    total: int
    page: int
    page_size: int
    items: list[JobResponse]

class StatsResponse(BaseModel):
    """Statistics response"""
    total_jobs: int
    categories: dict
    cities: dict
    job_types: dict
