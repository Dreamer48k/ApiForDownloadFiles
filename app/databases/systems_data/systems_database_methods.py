# import uuid
from asyncpg import Connection
from app.config import (SYSTEM_DATABASE_HOST_POSTGRES,
                        SYSTEM_DATABASE_PORT_POSTGRES,
                        SYSTEM_DATABASE_USERNAME_POSTGRES,
                        SYSTEM_DATABASE_PASSWORD_POSTGRES,
                        SYSTEM_DATABASE_NAME_POSTGRES,
                        SYSTEM_DATABASE_CONNECTION_COUNT_POSTGRES)
from app.databases.connections.asyncpg import AsyncpgConnectionGroup


class SystemsDatabase:
    connections = AsyncpgConnectionGroup(
        host=SYSTEM_DATABASE_HOST_POSTGRES,
        port=int(SYSTEM_DATABASE_PORT_POSTGRES),
        user=SYSTEM_DATABASE_USERNAME_POSTGRES,
        password=SYSTEM_DATABASE_PASSWORD_POSTGRES,
        database=SYSTEM_DATABASE_NAME_POSTGRES,
        connection_count=SYSTEM_DATABASE_CONNECTION_COUNT_POSTGRES
    )

    @classmethod
    async def get_user_path(cls, user_id):
        """Получить родительскую директорию пользователя"""
        connection: Connection
        async with cls.connections.get_free_connection() as connection:
            fetch_sql_command = f'''select
                parent_dir_path
                    from users_data.users_parent_dir upd
                where user_id = {user_id!r}'''
            free_id_count = await connection.fetch(fetch_sql_command)
        return [free_id for free_id, in free_id_count][0]
