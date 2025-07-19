from fastapi import APIRouter

router = APIRouter()

@router.post("/scan",
    summary="Start recon scan",
    response_model=dict,
)
async def start_scan(target: dict):
    """Stub endpoint to initiate Scammer (Recon AI) scan."""
    return {"message": "Scammer scan initiated", "target": target}

