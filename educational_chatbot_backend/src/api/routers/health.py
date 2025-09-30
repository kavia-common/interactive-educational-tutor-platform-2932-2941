from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", summary="Health Check", description="Return service health status.", responses={200: {"description": "Service is healthy"}})
def health_check():
    """Simple health check endpoint to verify service availability."""
    return {"message": "Healthy"}
