from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes import data
from src.helpers.config import settings

from src.story.llm.LLMProviderFactory import LLMProviderFactory
from src.routes.data import data_router
from src.routes import base

app = FastAPI()





async def startup_db_client():
    app.state.db_client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    app.state.db = app.state.db_client[settings.MONGO_DB_NAME]
    llm_provider_factory = LLMProviderFactory(settings)
    app.generation_provider = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_provider.set_generate_model(settings.GENERATION_MODEL_ID)
    app.embedding_provider = llm_provider_factory.create(settings.EMBEDDING_BACKEND)


async def shutdown_db_client():
    app.state.db_client.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)