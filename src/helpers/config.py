from pydantic_settings import BaseSettings, SettingsConfigDict
class Config(BaseSettings):
    App_NAME: str 
    App_DESCRIPTION: str
    App_VERSION: str   
    
    class Config:
        env_file = ".env"
        