from fastapi import FastAPI
from app.routers import ai

app = FastAPI()

app.include_router(ai.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PwnageBox"}
