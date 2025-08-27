import sys
import uvicorn
import asyncio
from app.config import TRASH_SERVER_API_HOST, TRASH_SERVER_API_PORT

if sys.platform == 'win32':
    # для работы bonsai на windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#
if __name__ == '__main__':
    uvicorn.run(
        'app.load:app',
        host=TRASH_SERVER_API_HOST,
        port=int(TRASH_SERVER_API_PORT),
        loop='asyncio',
        reload=True
    )
