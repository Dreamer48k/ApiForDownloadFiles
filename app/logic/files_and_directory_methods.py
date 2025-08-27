# переделать в отдельное хранилище и нормальный метод
import os
import asyncio


class FileDirMethods:
    sys_path = os.path.join(os.getcwd(), "data")

    @classmethod
    async def get_data_path(cls, path_user, user_login):
        """получить файлы и папки по указанному пути"""
        path_user = os.path.join(cls.sys_path, path_user)
        path_walk = os.walk(path_user)

        directores = []
        files = []

        for data in path_walk:
            await asyncio.sleep(0)
            print(data[0].split('\\'))
            if data[1] != []:
                directores.append(data[1])
            if data[2] != []:
                files.append(data[2])

        return {'directores': directores,
                'files': files}

    @classmethod
    async def get_files(cls, path):
        pass

    @classmethod
    async def get_dir(cls, path):
        pass
