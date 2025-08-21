import uvicorn

from app.config import TRASH_SERVER_API_HOST, TRASH_SERVER_API_PORT

#
if __name__ == '__main__':
    uvicorn.run(
        'app.load:app',
        host=TRASH_SERVER_API_HOST,
        port=int(TRASH_SERVER_API_PORT),
        loop='asyncio',
        reload=True
    )
