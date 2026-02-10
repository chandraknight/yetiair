import redis.asyncio as redis
from src.config import settings
from .singleton import Singleton

class RedisClient(metaclass=Singleton):
    def __init__(self):
        self._url = settings.REDIS_URL
        self._client = None

    async def connect(self):
        if not self._client:
            self._client = redis.from_url(self._url)

    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None
            
    async def get_client(self):
        if not self._client:
            await self.connect()
        return self._client
