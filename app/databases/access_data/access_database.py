# import uuid
from datetime import datetime
from asyncpg import Connection
from app.config import (ACCESS_DATABASE_HOST_POSTGRES,
                        ACCESS_DATABASE_PORT_POSTGRES,
                        ACCESS_DATABASE_USERNAME_POSTGRES,
                        ACCESS_DATABASE_PASSWORD_POSTGRES,
                        ACCESS_DATABASE_NAME_POSTGRES,
                        ACCESS_DATABASE_CONNECTION_COUNT_POSTGRES)
from app.databases.connections.asyncpg import AsyncpgConnectionGroup
#
from utils.security import Seccury


class AccessDatabase:
    connections = AsyncpgConnectionGroup(
        host=ACCESS_DATABASE_HOST_POSTGRES,
        port=int(ACCESS_DATABASE_PORT_POSTGRES),
        user=ACCESS_DATABASE_USERNAME_POSTGRES,
        password=ACCESS_DATABASE_PASSWORD_POSTGRES,
        database=ACCESS_DATABASE_NAME_POSTGRES,
        connection_count=ACCESS_DATABASE_CONNECTION_COUNT_POSTGRES
    )

    @classmethod
    async def get_last_free_id_in_table(cls, table_name):
        """Получить последний незанятый ID"""
        connection: Connection
        async with cls.connections.get_free_connection() as connection:
            fetch_sql_command = '''select
                count(id)+1 as free_id_count
            from access_data.users_data.''' + table_name
            free_id_count = await connection.fetch(fetch_sql_command)
        return [free_id for free_id, in free_id_count][0]

    @classmethod
    async def registration(cls,
                           user_login: str,
                           user_passwd: str,
                           user_name: str | None
                           ):
        """Регистрация пользователя"""
        connection: Connection

        free_id = await cls.get_last_free_id_in_table('users')

        if user_name is None or user_name == '':
            user_name = 'anon'
        is_deleted = False
        passwd_encrypted = await Seccury.hash_password(user_passwd)
        created_date = datetime.now()

        async with cls.connections.get_free_connection() as connection:
            return_id = await connection.fetch('''INSERT INTO users_data.users
                                     (id,
                                     user_login,
                                     user_name,
                                     passwd_encrypted,
                                     created_date,
                                     is_deleted)
                    values(
                        $1, $2, $3, $4, $5, $6
                    )
                    ON CONFLICT (user_login)
                    DO NOTHING
                RETURNING id;
            ''', free_id, user_login, user_name, passwd_encrypted, created_date, is_deleted)
            if len(return_id) > 0:
                return 'Registration Final'
            else:
                raise Exception("User is already exist")

    @classmethod
    async def get_user_authentication(cls,
                                      user_login: str,
                                      user_passwd: str):
        """получить сохраненый кэш пароля"""
        connection: Connection

        async with cls.connections.get_free_connection() as connection:
            hash_db_passwd = await connection.fetch(f'''
                    select passwd_encrypted from access_data.users_data.users
                    where user_login = {user_login!r}
                            and
                        is_deleted = false
                    ''')
            hash_db_passwd = [db_passwd for db_passwd, in hash_db_passwd][0]
            user_hash = await Seccury.verify_password(plain_password=user_passwd, hashed_password=hash_db_passwd)
            return user_hash

    @classmethod
    async def get_user_role_id(cls,
                               user_login: str):
        connection: Connection
        async with cls.connections.get_free_connection() as connection:

            role_id = await connection.fetch(f'''
                        select role_id  from users_data.user_role ur
                        inner join users_data.users u on u.id = ur.user_id
                                                            and u.user_login = {user_login!r}
                    ''')
            role_id = [id for id, in role_id][0]
            return role_id
