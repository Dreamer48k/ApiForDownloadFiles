from abc import ABC, abstractmethod
from time import time


class Connection(ABC):
    def __init__(self, host: str, port: int, user: str, password: str, database: str,
                 connection_lifetime: int | None = None):
        if connection_lifetime is None:
            connection_lifetime = 10 * 60

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection: ... = None
        self.lifetime = connection_lifetime
        self.refresh_time: float | None = None
        self.is_busy = False

    @abstractmethod
    async def is_connected(self) -> bool:
        pass

    @abstractmethod
    async def _create_connection(self) -> None:
        pass

    async def update(self) -> None:
        if self.refresh_time is None:
            return await self._create_connection()

        is_connection_active = await self.is_connected()

        if time() < self.refresh_time and is_connection_active:
            return self.connection

        if is_connection_active:
            await self.connection.close()

        return await self._create_connection()
