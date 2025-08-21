from uuid import UUID
from pydantic import BaseModel
from . import router_access


class UserUUID(BaseModel):
    uuid: UUID


@router_access.get('/get_user_access')
async def get_user_data_access(token_uuid: UserUUID):
    pass


# для active directory
@router_access.get('/get_ad_user_role')
async def get_user_group(token_uuid: UserUUID):
    """только для AD LDAP"""
    return
