from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    App_NAME: str
    App_DESCRIPTION: str
    App_VERSION: str
    FILE_EXTENSIONS: list
    FILE_MAX_SIZE: int = 10 
    FILE_CHUNK_SIZE: int = 51200
    MongoDB_URI: str 
    MongoDB_DB_NAME: str

    class Config:
        env_file = "./src/.env"

def get_settings():
    return Settings()
