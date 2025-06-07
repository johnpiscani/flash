"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FastAPI Agent Backend",
        "version": "1.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "FastAPI Agent Backend",
        "version": "1.0.0",
        "components": {
            "database": "healthy",  # Add actual database check
            "llm_service": "healthy",  # Add actual LLM service check
            "cache": "healthy"  # Add actual cache check
        }
    }