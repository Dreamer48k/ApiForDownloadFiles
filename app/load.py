# import asyncio

from fastapi import FastAPI
# , Request
# from fastapi.responses import  HTMLResponse
# from contextlib import asynccontextmanager
# from fastapi.middleware.cors import CORSMiddleware

# out_of_category
from importlib import import_module
from os.path import dirname
from pathlib import Path

# api methods
from .v1.api.admin import router_admin
from .v1.api.users import router_users
from .v1.api.access_systems import router_access
# from .v1.api.admin import *
# from .v1.api.users import *

API_FOLDERS = (
    'admin',
    'users',
    'access_systems'
)

app = FastAPI(
    title="MY_TRASH_API")


def load() -> None:
    for folder in API_FOLDERS:
        # await asyncio.sleep(0)
        modules = Path(dirname(__file__), 'v1/api', folder).glob('*.py')
        modules = [f.stem
                   for f in modules
                   if f.is_file() and f.name != '__init__.py']

        modules.sort()
        for module in modules:
            module = f'app.v1.api.{folder}.{module}'
            import_module(module)


async def lifespan(app: FastAPI):
    load()
    app.include_router(router_admin)
    app.include_router(router_users)
    app.include_router(router_access)
    yield

app = FastAPI(lifespan=lifespan)
