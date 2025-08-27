from pydantic import BaseModel
from . import router_access


class UserDataAcces(BaseModel):
    user_login: str
    user_passwd: str


# для active directory
@router_access.post('/get_ad_user_role')
async def get_user_group(user_data: UserDataAcces):
    """только для AD LDAP"""
    return
