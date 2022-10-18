from passlib.context import CryptContext
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from rich.console import Console
from rich.logging import RichHandler

import logging
import logstash

console = Console(color_system="256", width=150, style="blue")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@lru_cache
def get_logger(module_name):
    """

    Args:
        module_name:

    Returns:

    """ 
    host = 'logstash'
    port = 50000

    logger = logging.getLogger(module_name)
    logging.basicConfig(filename='general.log', encoding='utf-8', level=logging.DEBUG)
    
    # Create a handler for it
    handler = RichHandler(rich_tracebacks=True, console=console, tracebacks_show_locals=True)
    handler.setFormatter(logging.Formatter("%(name)s - [ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s"))

    # Add the handler to the logger
    logger.addHandler(logstash.LogstashHandler(host, port, version=1))
    logger.addHandler(handler)

    return logger


async def init_mongo(db_name: str, db_url: str, collection: str):
    """

    Args:
        db_name:
        db_url:
        collection:

    Returns:

    """
    mongo_client = AsyncIOMotorClient(db_url)
    mongo_database = mongo_client[db_name]
    mongo_collections = {
        collection: mongo_database.get_collection(collection),
    }
    # return {0: mongo_client, 1: mongo_database, 2: mongo_collections}
    return mongo_client, mongo_database, mongo_collections

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
