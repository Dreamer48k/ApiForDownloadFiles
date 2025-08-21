from app.databases.connections.abstract import ConnectionGroup
from .aiomysql_connection import AiomysqlConnection


class AiomysqlConnectionGroup(ConnectionGroup):
    @classmethod
    def _create_connection(cls, host: str, port: int, user: str, password: str, database: str,
                           connection_lifetime: int | None) -> AiomysqlConnection:
        return AiomysqlConnection(
            host=host, port=port, user=user, password=password, database=database,
            connection_lifetime=connection_lifetime
        )
