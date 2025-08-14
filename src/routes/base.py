from fastapi import FastAPI, APIRouter,Depends
from src.helpers.config import get_settings ,Settings

settings = get_settings()

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.App_NAME
    app_version = app_settings.App_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
