import aio_pika
from src.config import settings
from .singleton import Singleton

class RabbitMQClient(metaclass=Singleton):
    def __init__(self):
        self._url = settings.RABBITMQ_URL
        self._connection = None
        self._channel = None

    async def connect(self):
        if not self._connection:
            self._connection = await aio_pika.connect_robust(self._url)
            self._channel = await self._connection.channel()

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
            
    async def get_channel(self):
        if not self._channel:
            await self.connect()
        return self._channel
