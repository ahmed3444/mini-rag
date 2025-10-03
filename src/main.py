from fastapi import FastAPI
from src.routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.db = app.mongodb_client[settings.MONGO_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# <<< الخطوة 3: إضافة الـ Routers في النهاية >>>
app.include_router(base.base_router)
app.include_router(data.data_router)