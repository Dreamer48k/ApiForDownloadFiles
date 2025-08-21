import aiomysql
from time import time
from app.databases.connections.abstract import Connection


class AiomysqlConnection(Connection):
    def __init__(self, host: str, port: int, user: str, password: str, database: str,
                 connection_lifetime: int | None = None):
        super().__init__(
            host=host, port=port, user=user, password=password, database=database,
            connection_lifetime=connection_lifetime
        )
        self.connection: aiomysql.Cursor | None = None

    async def is_connected(self) -> bool:
        if self.connection is None or self.cursor is None:
            return False

        try:
            await self.cursor.execute('SELECT 1')
        except aiomysql.InterfaceError:
            return False

        return True

    async def _create_connection(self) -> aiomysql.Connection:
        self.connection = await aiomysql.connect(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            db=self.database
        )
        self.cursor = await self.connection.cursor()
        self.refresh_time = time() + self.lifetime

        return self.cursor
