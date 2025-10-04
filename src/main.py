from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings  # لو عندك إعدادات كده

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.state.db_client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.state.db = app.state.db_client[settings.MONGO_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.db_client.close() 