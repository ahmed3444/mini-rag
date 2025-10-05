from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import settings

# ✅ استيراد الراوتر
from src.routes.data import data_router

app = FastAPI()

# ✅ تسجيل الراوتر
app.include_router(data_router)

@app.on_event("startup")
async def startup_db_client():
    app.state.db_client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.state.db = app.state.db_client[settings.MONGO_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.db_client.close()
