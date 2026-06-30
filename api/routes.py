"""API routes"""
import logging
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import func
from scraper.database import get_session, Job
from api.models import JobResponse, JobListResponse, StatsResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["jobs"])

@router.get("/jobs", response_model=JobListResponse)
def get_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    city: str = Query(None),
    job_type: str = Query(None)
):
    """Get paginated jobs with optional filters"""
    try:
        session = get_session()
        query = session.query(Job)
        
        # Apply filters
        if category:
            query = query.filter(Job.category.ilike(f"%{category}%"))
        if city:
            query = query.filter(Job.city.ilike(f"%{city}%"))
        if job_type:
            query = query.filter(Job.job_type.ilike(f"%{job_type}%"))
        
        # Count total
        total = query.count()
        
        # Pagination
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return JobListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=[JobResponse.model_validate(item) for item in items]
        )
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        session.close()

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    """Get specific job by ID"""
    try:
        session = get_session()
        job = session.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobResponse.model_validate(job)
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        session.close()

@router.get("/jobs/search", response_model=JobListResponse)
def search_jobs(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Search jobs by title or description"""
    try:
        session = get_session()
        query = session.query(Job).filter(
            (Job.title.ilike(f"%{q}%")) | (Job.description.ilike(f"%{q}%"))
        )
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return JobListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=[JobResponse.model_validate(item) for item in items]
        )
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        session.close()

@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """Get statistics about jobs"""
    try:
        session = get_session()
        
        # Total jobs
        total_jobs = session.query(func.count(Job.id)).scalar() or 0
        
        # Jobs by category
        categories = dict(
            session.query(Job.category, func.count(Job.id))
            .group_by(Job.category)
            .all()
        )
        
        # Jobs by city
        cities = dict(
            session.query(Job.city, func.count(Job.id))
            .group_by(Job.city)
            .all()
        )
        
        # Jobs by type
        job_types = dict(
            session.query(Job.job_type, func.count(Job.id))
            .group_by(Job.job_type)
            .all()
        )
        
        return StatsResponse(
            total_jobs=total_jobs,
            categories=categories,
            cities=cities,
            job_types=job_types
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        session.close()
