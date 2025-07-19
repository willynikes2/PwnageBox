from fastapi import APIRouter

router = APIRouter()

@router.get("",
    summary="Health check",
    response_model=dict,
)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

