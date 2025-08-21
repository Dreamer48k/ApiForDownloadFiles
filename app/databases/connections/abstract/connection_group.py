import asyncio
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator

# import asyncpg

from .connection import Connection
from .exceptions import WaitFreeConnectionTimeoutError


class ConnectionGroup(ABC):
    _get_free_connection_attempt_wait_time = 0.1

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 database: str,
                 connection_count: int = 2,
                 connection_lifetime: int | None = None,
                 max_free_connection_wait_time: int = 10):
        self._max_free_connection_wait_time = max_free_connection_wait_time
        self._connections = [
            self._create_connection(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connection_lifetime=connection_lifetime,
            )
            for _ in range(connection_count)
        ]

    @classmethod
    @abstractmethod
    def _create_connection(cls,
                           host: str,
                           port: int,
                           user: str,
                           password: str,
                           database: str,
                           connection_lifetime: int | None) -> Connection:
        pass

    @asynccontextmanager
    async def get_free_connection(self) -> AsyncIterator[Connection]:
        free_connection: Connection | None = None

        for _ in range(int(self._max_free_connection_wait_time / self._get_free_connection_attempt_wait_time)):
            for connection in self._connections:
                if not connection.is_busy:
                    connection.is_busy = True
                    free_connection = connection
                    break

            if free_connection is not None:
                break

            await asyncio.sleep(self._get_free_connection_attempt_wait_time)

        if free_connection is None:
            raise WaitFreeConnectionTimeoutError()

        try:
            await free_connection.update()
            yield free_connection.connection
        finally:
            free_connection.is_busy = False

    def get_connection_statuses(self) -> list[str]:
        return ['busy' if connection.is_busy else 'free' for connection in self._connections]
