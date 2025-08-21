import asyncio
# from typing import Tuple
from passlib.context import CryptContext
from fastapi.concurrency import run_in_threadpool


class Seccury:
    passwd_context = CryptContext(
        schemes=["argon2"],
        deprecated="auto"
    )

    @classmethod
    async def hash_password(cls,
                            password: str) -> str:
        return await run_in_threadpool(cls.passwd_context.hash, password)

    @classmethod
    async def verify_password(cls,
                              plain_password: str,
                              hashed_password: str) -> bool:
        return await run_in_threadpool(cls.passwd_context.verify, plain_password, hashed_password)


if __name__ == '__main__':
    test_sec = Seccury()

    async def test():
        hash = await test_sec.hash_password('test')
        print(hash)

        print(
            await test_sec.verify_password('test', hash)
        )

    asyncio.run(test())
