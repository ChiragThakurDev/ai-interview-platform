from fastapi import FastAPI
from app.core.config import settings

app=FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        )

@app.get("/")
async def root():
    return{
            "message": f"Welcome to {settings.app_name}"
            }

@app.get("/health")
async def health_check():
    return{
            "status":"healthy"
            }

