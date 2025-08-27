# import uuid
from datetime import datetime
from asyncpg import Connection
from app.config import (SYSTEM_DATABASE_HOST_POSTGRES,
                        SYSTEM_DATABASE_PORT_POSTGRES,
                        SYSTEM_DATABASE_USERNAME_POSTGRES,
                        SYSTEM_DATABASE_PASSWORD_POSTGRES,
                        SYSTEM_DATABASE_NAME_POSTGRES,
                        SYSTEM_DATABASE_CONNECTION_COUNT_POSTGRES)
from app.databases.connections.asyncpg import AsyncpgConnectionGroup
#
from utils.security import Seccury


class AccessDatabase:
    connections = AsyncpgConnectionGroup(
        host=SYSTEM_DATABASE_HOST_POSTGRES,
        port=int(SYSTEM_DATABASE_PORT_POSTGRES),
        user=SYSTEM_DATABASE_USERNAME_POSTGRES,
        password=SYSTEM_DATABASE_PASSWORD_POSTGRES,
        database=SYSTEM_DATABASE_NAME_POSTGRES,
        connection_count=SYSTEM_DATABASE_CONNECTION_COUNT_POSTGRES
    )

    @classmethod
    async def get_last_free_id_in_table(cls, table_name):
        """Получить последний незанятый ID"""
        connection: Connection
        async with cls.connections.get_free_connection() as connection:
            fetch_sql_command = '''select
                count(id)+1 as free_id_count
            from users_data.''' + table_name
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
            if len(return_id) <= 0:
                raise Exception("User is already exist")

            # переделать!
            sql_command_create_path_and_role = f'''
            with  user_role as (
                    INSERT INTO users_data.user_role
                            (user_id, role_id)
                            VALUES({free_id!r}, 1)
                            RETURNING 1 as result_user_role
                ),
                user_parent_dir as (
                    INSERT INTO users_data.users_parent_dir
                        (user_id,
                        parent_dir_path)
                        values(
                                {free_id!r}, {user_login!r}
                            )
                            RETURNING 1 as  result_user_parent_dir
                )
                select result_user_role, result_user_parent_dir from   user_role
                left join user_parent_dir on 1=1;
            '''
            result_created_user_data = await connection.fetch(sql_command_create_path_and_role)
            result_created_user_data = [dict(data) for data in result_created_user_data][0]
            if len(result_created_user_data.keys()) != 2:
                raise Exception("Create user data is error")

            for key in result_created_user_data:
                if result_created_user_data[key] != 1:
                    raise Exception(f"Create user {key!r} is error")

            return 'Success'

    @classmethod
    async def get_user_authentication(cls,
                                      user_login: str,
                                      user_passwd: str):
        """получить сохраненый кэш пароля"""
        connection: Connection

        async with cls.connections.get_free_connection() as connection:
            # переделать!!
            hash_db_passwd = await connection.fetch(f'''
                    select passwd_encrypted from users_data.users
                    where user_login = {user_login!r}
                            and
                        is_deleted = false
                    ''')
            if hash_db_passwd == []:
                raise [False, 'User not Register']

            hash_db_passwd = [db_passwd for db_passwd, in hash_db_passwd][0]
            user_hash = await Seccury.verify_password(plain_password=user_passwd, hashed_password=hash_db_passwd)
            if not user_hash:
                return [False, 'Access Denied']
            return [user_hash]

    @classmethod
    async def get_user_id_and_role_id(cls, user_login: str):
        connection: Connection
        async with cls.connections.get_free_connection() as connection:

            user_data = await connection.fetch(f'''
                        select user_id, role_id  from users_data.user_role ur
                        inner join users_data.users u on u.id = ur.user_id
                                                            and u.user_login = {user_login!r}
                    ''')
            if user_data == []:
                raise 'User Data Not Found'
            temp_user_data = {}
            if len(user_data) > 1:
                temp_data = [dict(data)['role_id'] for data in user_data]
                temp_user_data['user_id'] = dict(user_data[0])['user_id']
                temp_user_data['role_id'] = temp_data
                temp_user_data[user_login] = temp_user_data
                return temp_user_data

            temp_user_data[user_login] = dict(user_data[0])
            return temp_user_data
