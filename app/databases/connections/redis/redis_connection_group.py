from app.databases.connections.abstract import ConnectionGroup
from .redis_connection import RedisConnection


class RedisConnectionGroup(ConnectionGroup):
    @classmethod
    def _create_connection(cls, host: str, port: int, user: str, password: str, database: str,
                           connection_lifetime: int | None) -> RedisConnection:
        return RedisConnection(
            host=host, port=port, user=user, password=password, database=database,
            connection_lifetime=connection_lifetime
        )
