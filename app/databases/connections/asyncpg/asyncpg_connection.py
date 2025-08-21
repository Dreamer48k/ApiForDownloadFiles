import asyncpg
from time import time
from app.databases.connections.abstract import Connection


class AsyncpgConnection(Connection):
    async def is_connected(self) -> bool:
        if self.connection is None:
            return False

        try:
            await self.connection.fetch('SELECT 1')
        except asyncpg.InterfaceError:
            return False

        return True

    async def _create_connection(self) -> asyncpg.Connection:
        self.connection = await asyncpg.connect(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            database=self.database
        )
        self.refresh_time = time() + self.lifetime

        return self.connection
