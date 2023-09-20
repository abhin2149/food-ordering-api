from utils.config import get_config
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


def mongo_engine():
    config = get_config()
    client = AsyncIOMotorClient(config["MONGODB_CONNECTION_URI"])
    engine = AIOEngine(client=client, database=config["DB_NAME"])
    return engine

