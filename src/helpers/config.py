from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    App_NAME: str 
    App_DESCRIPTION: str
    App_VERSION: str   

    class Config:
        env_file = ".env"

def get_settings() :
    return Settings()

