# import pandas as pd
# from uuid import UUID
# from fastapi.responses import JSONResponse
from . import router_admin

# from pydantic import BaseModel
# from os import walk

# class PathData(BaseModel):
#     path : str


@router_admin.get('/xxx')
async def get_all_pages_names(path: str):
    path = path
    # pages_name = await DB_SYS.get_all_page_names()
    # pages_name = pages_name[0]['page_name']
    pass
