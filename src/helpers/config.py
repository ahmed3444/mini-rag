from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    FILE_EXTENSIONS: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    MONGO_DB_URI: str
    MONGO_DB_NAME: str

    class Config:
        env_file = "src/.env"
        env_file_encoding = 'utf-8'

settings = Settings()

def get_settings():
    return settings