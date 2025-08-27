# import aiofiles

from uuid import UUID
from fastapi.responses import (JSONResponse)
# StreamingResponse,)

from . import router_users
from app.databases.systems_data import SystemsDatabase
from app.databases.access_data.access_database_redis_methods import AccessTokenDatabase
from app.logic.files_and_directory_methods import FileDirMethods


@router_users.get('/get_user_directories')
async def get_user_directories(uuid_user_session: UUID):
    """Данные из папки пользователя только по файлам \n
    Data from user folder only by files"""
    uuid_user_session = str(uuid_user_session)
    user_data = await AccessTokenDatabase.get_user_token_in_db(uuid_session=uuid_user_session)
    user_login = user_data[b'login'].decode('utf-8')
    user_id = user_data[b'user_id'].decode('utf-8')
    path = await SystemsDatabase.get_user_path(user_id)
    data_path = await FileDirMethods.get_data_path(path_user=path, user_login=user_login)

    # df = pd.DataFrame(data_files, columns=['path','dirs','files'])
    # print(df)
    return JSONResponse(
                status_code=200,
                content={'path': path,
                         'directores': data_path['directores'],
                         'files': data_path['files']})
