from uuid import UUID
# UUID,
from . import router_access
from pydantic import BaseModel
# from utils.print_system import async_debug_console_print
from app.databases.access_data.access_database_methods import AccessDatabase
from app.databases.access_data.access_database_redis_methods import AccessTokenDatabase
from app.logic.models.api_responses import ResponseError, ResponseSuccess


class UserDataAcces(BaseModel):
    user_login: str
    user_passwd: str


class UserDataRegistration(BaseModel):
    user_login: str
    user_passwd: str
    user_name: str | None


@router_access.post('/user_auth')
async def user_auth(user_data: UserDataAcces):
    try:
        user_login = user_data.user_login
        user_passwd = user_data.user_passwd
        isUser = await AccessDatabase.get_user_authentication(
            user_login=user_login,
            user_passwd=user_passwd
        )
        if isUser[0]:
            token_uuid = await AccessTokenDatabase.set_user_token_in_db(user_data.user_login)
            return ResponseSuccess(
                content={'uuid4': str(token_uuid)}
            )
        else:
            return ResponseError(
                status_code=403,
                message={'Error': isUser[1]}
            )

    except Exception as Error:
        return ResponseError(
            status_code=500,
            message={'Error': Error}
        )


@router_access.post('/registration_user')
async def registration_user(user_data: UserDataRegistration):
    try:
        user_login = user_data.user_login
        user_passwd = user_data.user_passwd
        user_name = user_data.user_name

        message = await AccessDatabase.registration(
            user_login=user_login,
            user_passwd=user_passwd,
            user_name=user_name
        )

        return ResponseSuccess(
            content={'message': message}
        )
    except Exception as Error:
        # await async_debug_console_print(
        #     'ResponseError', str(Error)
        # )
        return ResponseError(
            status_code=500,
            message=str(Error)
        )


# разбить на разные части!!!
@router_access.get('/get_user_data')
async def get_user_data(token_uuid: UUID):
    token_uuid = str(token_uuid)
    try:
        data_user = await AccessTokenDatabase.get_user_token_in_db(token_uuid)
        if data_user == 'No' or data_user == {}:
            return ResponseError(
                status_code=403,
                message='Session is Dead or UUID no valid'
            )
        data_user = {k.decode('utf-8'): v.decode('utf-8') for k, v in data_user.items()}
        return ResponseSuccess(
            content={'message': data_user}
        )
    except Exception as Error:
        return ResponseError(
                status_code=500,
                message=str(Error)
            )
    # await AccessTokenDatabase.update_time_token(token_uuid)
    # await AccessTokenDatabase.get_user_token_in_db(token_uuid)
