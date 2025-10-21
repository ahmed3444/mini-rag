import json
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    MONGO_DB_URI: str
    MONGO_DB_NAME: str
    
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    
    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None
    
    class Config:
        env_file = ".env"
    
    def get_settings():
        return Settings()

    # النوع الأساسي
    FILE_ALLOWED_TYPES: list = Field(default_factory=lambda: [
        "text/plain",
        "application/pdf",
        "application/json",
        "text/csv"
    ])

    class Config:
        env_file = "src/.env"
        env_file_encoding = 'utf-8'

 
    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.FILE_ALLOWED_TYPES, str):
            try:
                self.FILE_ALLOWED_TYPES = json.loads(self.FILE_ALLOWED_TYPES)
            except json.JSONDecodeError:
                self.FILE_ALLOWED_TYPES = self.FILE_ALLOWED_TYPES.split(",")

settings = Settings()

def get_settings():
    return settings
