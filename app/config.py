from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "default_secret"
    app_name: str = "GearOptimizer API"
    app_version: str = "3.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"

@lru_cache()        
def get_settings() -> Settings:
    return Settings()
