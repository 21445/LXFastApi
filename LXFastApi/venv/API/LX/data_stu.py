import asyncio
from tortoise import Tortoise, run_async
from model20 import User

async def create_users(id: str, username: str, email: str, is_active: bool = True):


    user = await User.create(
        id=id,
        username=username,
        email=email,
        is_active=is_active,
    )
    return user

async def init():
    await Tortoise.init(
        db_url="mysql://root:root@127.0.0.1:3307/fastapi_db2",
        modules={"models": ["model20"]},
       
    )

async def main():
    await init()
    await create_users("123456", "testuser", "test@example.com",)
    await create_users("654321", "testuser2", "test2@example.com",)
    await create_users("123567", "testuser43", "test34@example.com")
 



if __name__ == "__main__":
    run_async(main())




