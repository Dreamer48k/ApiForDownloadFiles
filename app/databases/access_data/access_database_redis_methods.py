import redis.asyncio as redis
import json
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from app.config import (ACCESS_DATABASE_HOST_REDIS,
                        ACCESS_DATABASE_PORT_REDIS,
                        ACCESS_DATABASE_USERNAME_REDIS,
                        ACCESS_DATABASE_PASSWORD_REDIS,
                        ACCESS_DATABASE_NAME_REDIS,
                        ACCESS_DATABASE_CONNECTION_COUNT_REDIS)
from app.databases.connections.redis import RedisConnectionGroup
from .access_database_methods import AccessDatabase
#
# from utils.security import Seccury


class AccessTokenDatabase:
    connections = RedisConnectionGroup(
        host=ACCESS_DATABASE_HOST_REDIS,
        port=int(ACCESS_DATABASE_PORT_REDIS),
        user=ACCESS_DATABASE_USERNAME_REDIS,
        password=ACCESS_DATABASE_PASSWORD_REDIS,
        database=ACCESS_DATABASE_NAME_REDIS,
        connection_count=ACCESS_DATABASE_CONNECTION_COUNT_REDIS
    )

    @classmethod
    async def set_user_token_in_db(cls,
                                   login: str):
        """Создать токен на вход"""
        connection: redis

        user_data = await AccessDatabase.get_user_id_and_role_id(login)
        user_data = {'login': login,
                     'user_id': user_data[login]['user_id'],
                     'role_id':  json.dumps(user_data[login]['role_id']),
                     'b_datetime': datetime.timestamp(datetime.now()),
                     'e_datetime':  datetime.timestamp(datetime.now()+timedelta(minutes=15))}
        uuid_session = str(uuid4())
        async with cls.connections.get_free_connection() as connection:
            await connection.hset(uuid_session, mapping=user_data)
        return uuid_session

    @classmethod
    async def get_user_token_in_db(cls,
                                   uuid_session: UUID):
        """Получить данные сессии пользовтеля"""
        connection: redis
        uuid_session = str(uuid_session)
        async with cls.connections.get_free_connection() as connection:
            session_data = await connection.hgetall(uuid_session)
            if not session_data:
                raise Exception('session_data is none')
            return session_data

    @classmethod
    async def update_time_token(cls,
                                uuid_session: UUID):
        """Обновляем время жизни uuid-а сессии"""
        connection: redis

        # нужно, если токен стух и воззваращать на страницу хода
        end_token_time = await cls.get_user_token_in_db(uuid_session=uuid_session)
        if end_token_time != {}:
            end_token_time = float(end_token_time[b'e_datetime'])
        else:
            return 'No'
        #

        lifetime_uuid = {'b_datetime': datetime.timestamp(datetime.now()),
                         'e_datetime': datetime.timestamp(datetime.now()+timedelta(minutes=15))}

        async with cls.connections.get_free_connection() as connection:
            if datetime.timestamp(datetime.now()) >= end_token_time:
                await connection.delete(uuid_session)
                return 'No'
            await connection.hset(uuid_session, mapping=lifetime_uuid)
