from app.databases.connections.abstract import ConnectionGroup
from .asyncpg_connection import AsyncpgConnection


class AsyncpgConnectionGroup(ConnectionGroup):
    @classmethod
    def _create_connection(cls, host: str, port: int, user: str, password: str, database: str,
                           connection_lifetime: int | None) -> AsyncpgConnection:
        return AsyncpgConnection(
            host=host, port=port, user=user, password=password, database=database,
            connection_lifetime=connection_lifetime
        )
