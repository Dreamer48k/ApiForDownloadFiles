import os
# import aiofiles

from uuid import UUID
from fastapi.responses import (JSONResponse)
# StreamingResponse,)

from . import router_users


@router_users.get('/get_data_directories')
async def get_data_directories(
                            # времменое решение
                            path: str,
                            uuid_user_session: UUID
                            ):
    """Данные из папки пользователя только по файлам \n
    Data from user folder only by files"""
    # pages_name = await DataLake.get_all_page_names()
    # pages_name = pages_name[0]['page_name']

    # path получать из бд
    path_walk = os.walk(path)
    directores = []
    files = []
    for data in path_walk:
        print(data)
        directores.append(data[1])
        files.append(data[2])
        # break
    # df = pd.DataFrame(data_files, columns=['path','dirs','files'])
    # print(df)

    return JSONResponse(
                status_code=200,
                content={'path': path,
                         'directores': directores,
                         'files': files})
