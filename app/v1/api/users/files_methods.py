import os
import aiofiles
# import asyncio

from uuid import UUID

# fastapi methods
from fastapi import UploadFile
from fastapi.responses import (JSONResponse,
                               StreamingResponse,)

# from urllib.parse import unquote
# from pydantic import BaseModel

from . import router_users
from utils.print_system import debug_console_print


# class PathData(BaseModel):
#     path : str

CHUNK_SIZE = 1024 * 1024
data_file_dict = dict()


@router_users.get('/get_data_files')
async def get_data_files(
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
        # print(data)
        debug_console_print(data, data)
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


@router_users.get("/download_file")
async def download_file(path: str):
    file_name = path.split('\\')
    file_name = file_name[len(file_name)-1]

    async def iterfile():
        async with aiofiles.open(path, 'rb') as f:
            while chunk := await f.read(CHUNK_SIZE):
                yield chunk

    headers = {
            'Content-Disposition':
            'attachment; filename="{file_name}"'.format(file_name=file_name)
               }
    return StreamingResponse(iterfile(),
                             headers=headers,
                             media_type="multipart/form-data")
    # return FileResponse(path=path,
    # filename=file_name, media_type='multipart/form-data')


@router_users.post("/upload_file")
async def upload_file(file: UploadFile):
    dir_system_path = os.path.dirname(os.path.realpath(__file__))  # в дальнейшем брать path из бд
    # ut_file_path = r'J:\Projects\Python\my_download_site\data\\'
    ut_file_path = os.path.join(dir_system_path, 'data')
    number_chunk = 0
    id_file = '2x'
    debug_console_print('file_path', ut_file_path+file.filename)
    async with aiofiles.open(ut_file_path+file.filename, 'wb') as out_file:
        while content := await file.read(CHUNK_SIZE):
            # print(content)
            number_chunk += 1
            await out_file.write(content)
            await progress_bar(number_chunk, id_file)
    del number_chunk
    # return Response(file.file.read(), media_type=file.content_type)
    # out_file_path = r'J:\Projects\Python\my_download_site\data'
    # async with aiofiles.open(out_file_path, 'wb') as out_file:
    #     while content := await in_file.read(1024):  # async read chunk
    #         await out_file.write(content)  # async write chunk
    # return {"Result": "OK"}


async def progress_bar(number: int, id_file: str):
    # print('number_chank:', number, 'mb')
    # print(id_file, ': ', number)
    data_file_dict[id_file] = number
    # await asyncio.sleep(0)


@router_users.get("/get_chank")
def get_progress_bar(id: str):

    print(data_file_dict)
    response_bar = -1
    try:
        response_bar = data_file_dict[id]
        print(data_file_dict[id])
        del data_file_dict[id]
        return JSONResponse(
            status_code=200,
            content={'id': id,
                     'progress_bar': response_bar})

    except Exception as err:
        print('err:', err)

        return JSONResponse(
            status_code=500,
            content={'id': id,
                     'progress_bar': response_bar})
