from fastapi.responses import JSONResponse


class ResponseSuccess(JSONResponse):
    def __init__(self, status_code: int = 200, content: ... = None):
        if content is None:
            content = {'result': 'ok'}

        super().__init__(content, status_code)


class ResponseError(JSONResponse):
    def __init__(self, status_code: int, message: str):
        super().__init__(
            {
                'error': {
                    'status_code': status_code,
                    'message': message
                }
            },
            status_code
        )


__all__ = (
    'ResponseSuccess',
    'ResponseError',
)
