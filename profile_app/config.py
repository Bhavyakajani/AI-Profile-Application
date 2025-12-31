from functools import lru_cache
from typing import Optional
from fastapi import FastAPI

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Profile Application"
    admin_email: str = "kajanibhavya@gmail.com"
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env")

class GlobalConfig(Settings):
    MONGODB_URI: str = None
    DB_FORCE_ROLLBACK: bool = False
    USERS_COLLECTION: str ="users"
    CANDIDATES_COLLECTION: str ="candidates"
    DB_NAME: str = None

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

class TestConfig(GlobalConfig):
    DB_FORCE_ROLLBACK: bool = True
    MONGODB_URI: str ="mongodb://localhost:27017/"
    DB_NAME: str ="ProfileDB_TEST"
    model_config = SettingsConfigDict(env_prefix="TEST_")

class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")

@lru_cache
def get_config(env_state: str) -> GlobalConfig:
    configs = {
        "dev": DevConfig,
        "test": TestConfig,
        "prod": ProdConfig
    }

    return configs[env_state.lower()]()

config = get_config(Settings().ENV_STATE)
print(f"Loaded configuration for environment: {str(config)}")