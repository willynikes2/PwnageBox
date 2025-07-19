from fastapi import APIRouter

router = APIRouter()

@router.post("/execute",
    summary="Execute exploit",
    response_model=dict,
)
async def execute(target_id: str, goal: str):
    """Stub endpoint to execute an exploit with the Pwner engine."""
    return {"message": "Pwner execution started", "target_id": target_id, "goal": goal}

