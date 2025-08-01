from fastapi import FastAPI, APIRouter
from src.helpers.config import get_settings 

settings = get_settings()

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome():
    app_name = settings.App_NAME
    app_version = settings.App_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
