# dbConnect.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

    @classmethod
    async def connect(cls, uri: str, db_name: str):
        try:
            cls.client = AsyncIOMotorClient(uri)
            cls.database = cls.client[db_name]
            print(f"Connected to MongoDB database: {db_name}")
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")

    @classmethod
    async def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")

# Usage example:
# await MongoDB.connect("mongodb://localhost:27017", "your_database_name")
# await MongoDB.disconnect()
