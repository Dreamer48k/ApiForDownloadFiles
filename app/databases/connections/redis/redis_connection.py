import redis.asyncio as redis
from time import time
from app.databases.connections.abstract import Connection


class RedisConnection(Connection):
    async def is_connected(self) -> bool:
        if self.connection is None:
            return False

        try:
            await self.connection.ping()
        except Exception as ErrorConnection:
            print('\n\nErrorConnection', ':', ErrorConnection, '\n\n\n')
            return False
        return True

    async def _create_connection(self) -> redis.Redis:
        self.connection = await redis.Redis(
            host=self.host, port=self.port,
            username=self.user, password=self.password,
            db=self.database
        )
        self.refresh_time = time() + self.lifetime

        return self.connection
