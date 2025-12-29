from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Content Orchestrator"
    API_V1_STR: str = "/v1"
    
    # Supabase / Database
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    
    # Storage
    STORAGE_TYPE: str = "local" # or supabase
    LOCAL_STORAGE_PATH: str = "downloads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
