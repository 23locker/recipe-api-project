import json
from datetime import datetime
from typing import Any, Optional
from redis import asyncio as aioredis
from app.config import settings

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class RedisService:
    def __init__(self):
        self._redis: Optional[aioredis.Redis] = None

    async def get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return self._redis

    async def set(self, key: str, value: Any, expire: int = 3600):
        redis = await self.get_redis()
        await redis.set(key, json.dumps(value, cls=DateTimeEncoder), ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        redis = await self.get_redis()
        data = await redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def delete(self, key: str):
        redis = await self.get_redis()
        await redis.delete(key)

    async def delete_by_pattern(self, pattern: str):
        redis = await self.get_redis()
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)

redis_service = RedisService()
