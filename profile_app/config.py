from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(_ENV_PATH)

"""
Configure an envoironment:
1. create a sub-class of GlobalConfig named <EnvName>Config
2. Set the model config from SettingsConfigDict with env_prefix="<ENVNAME>_"
3. Add necessary variables like DB_URI, DB_NAME, Collection names either in ENV file or if to be kept constant throughout environments, set them in the class directly.
4. Add the class to the configs dict in get_config function.
"""

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
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017

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
def get_config(env_state: Optional[str] = None) -> GlobalConfig:
    print(f"Detecting environment: {env_state}")
    configs = {
        "dev": DevConfig,
        "test": TestConfig,
        "prod": ProdConfig
    }

    return configs[env_state.lower()]()

config = get_config(Settings().ENV_STATE)