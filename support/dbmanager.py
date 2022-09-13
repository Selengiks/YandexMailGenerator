import pymongo
from pymongo import errors
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import mongo_uri, mongo_db

class FastMongo:
    """
    Need to close Mongo client connections when shutdown
    await FastMongo.close()
    await FastMongo.wait_closed()
    """

    def __init__(self):
        self._db = None
        self._mongo = None

    def get_client(self) -> AsyncIOMotorClient:
        if isinstance(self._mongo, AsyncIOMotorClient):
            return self._mongo
        try:
            self._mongo = AsyncIOMotorClient(mongo_uri)
        except pymongo.errors.ConfigurationError as e:
            if "query() got an unexpected keyword argument 'lifetime'" in e.args[0]:
                logger.warning("Run `pip install dnspython==1.16.0` in order to fix ConfigurationError. "
                               "More information: https://github.com/mongodb/mongo-python-driver/pull/423#issuecomment-528998245")
            raise e
        return self._mongo

    def get_db(self) -> AsyncIOMotorDatabase:
        """
        Get mongo db
        """
        if isinstance(self._db, AsyncIOMotorDatabase):
            return self._db

        mongo = self.get_client()
        self._db = mongo.get_database(mongo_db)

        return self._db

    async def close(self):
        if self._mongo:
            self._mongo.close()

    async def wait_closed(self):
        return True

mongo = FastMongo()
