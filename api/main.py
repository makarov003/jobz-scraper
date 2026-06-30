"""FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config
from api.routes import router
from scraper.utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="jobz-scraper API",
    description="API for jobz.az job scraping platform",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "jobz-scraper API",
        "version": "0.1.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.API_DEBUG
    )
