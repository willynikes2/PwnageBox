from fastapi import APIRouter

router = APIRouter()

@router.get("/generate",
    summary="Generate vulnerability report",
    response_model=dict,
)
async def generate_report():
    """Stub endpoint to generate a vulnerability report."""
    return {"message": "Report generation started"}

