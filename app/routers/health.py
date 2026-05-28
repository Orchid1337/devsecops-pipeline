from fastapi import APIRouter

from app.models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Used as k8s liveness probe."""
    return HealthResponse()


@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """Used as k8s readiness probe."""
    return HealthResponse(status="ready")
