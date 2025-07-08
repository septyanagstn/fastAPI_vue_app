from motor.motor_asyncio import AsyncIOMotorClient

Mongo_URI = "mongodb://localhost:27017"

client = AsyncIOMotorClient(Mongo_URI)
database = client["kabayan"]    # Change with your Database name