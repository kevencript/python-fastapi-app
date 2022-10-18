import os
from functools import lru_cache

from pydantic import BaseSettings

from embed.utils import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    """

    BaseSettings, from Pydantic, validates the data so that when we create an instance of Settings,
    environment and testing will have types of str and bool, respectively.

    Parameters:


    Returns:
    instance of Settings

    """
    # Env Configs
    environment: str = os.getenv("ENVIRONMENT", "local")
    testing: str = os.getenv("TESTING", "0")
    up: str = os.getenv("UP", "up")
    down: str = os.getenv("DOWN", "down")
    web_server: str = os.getenv("WEB_SERVER", "web_server")

    # MongoDB Configs
    db_url: str = os.getenv("MONGO_URL", "")
    db_name: str = os.getenv("MONGO_DB", "")
    collection: str = os.getenv("MONGO_COLLECTION", "")
    test_db_name: str = os.getenv("MONGO_TEST_DB", "")

    # JWT Authentication Configs
    JWT_PUBLIC_KEY: str = os.getenv("JWT_PUBLIC_KEY", "")
    JWT_PRIVATE_KEY: str = os.getenv("JWT_PRIVATE_KEY", "")
    REFRESH_TOKEN_EXPIRES_IN: int = os.getenv("REFRESH_TOKEN_EXPIRES_IN", "")
    ACCESS_TOKEN_EXPIRES_IN: int = os.getenv("ACCESS_TOKEN_EXPIRES_IN", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "")
    CLIENT_ORIGIN: str = os.getenv("CLIENT_ORIGIN", "")


@lru_cache
def get_settings():
    logger.info("Loading config settings from the environment...")
    return Settings()
