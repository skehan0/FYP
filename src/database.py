import os
from motor.motor_asyncio import AsyncIOMotorClient

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            MONGO_URI = os.getenv("MONGO_URI")
            print("Connecting to MongoDB...")
            self.client = AsyncIOMotorClient(MONGO_URI)
            self.db = self.client['tradely']
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print("Error connecting to MongoDB:", str(e))
            raise e

    async def get_collection(self, collection_name):
        """Get a collection from the database."""
        if not self.db:
            await self.connect()
        return self.db[collection_name]
    
    async def get_db(self):
        """Ensure database connection is established before use."""
        if not self.db:
            await self.connect()
        return self.db

# Create an instance of DatabaseManager
database = DatabaseManager()