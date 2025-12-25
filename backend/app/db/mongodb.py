from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None


async def init_mongodb():
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URL)
        _db = _client[settings.MONGODB_DB]
        print(f"✅ Connected to MongoDB - {settings.MONGODB_DB}")


async def get_mongodb() -> AsyncIOMotorDatabase:
    if _db is None:
        await init_mongodb()
    return _db


async def close_mongodb():
    global _client
    if _client:
        _client.close()
        print("❌ Close MongoDB connection")
