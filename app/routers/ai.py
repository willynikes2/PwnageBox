```python
from fastapi import APIRouter
from app.ai_modules import example

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/example")
async def get_example():
    result = example.run_example()
    return {"result": result}
```
