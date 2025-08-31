import asyncio

from db.connector import get_session
from scheduler import scheduler_loop


async def main():
    await asyncio.sleep(10)

    async for session in get_session():
        await scheduler_loop(session)


if __name__ == "__main__":
    asyncio.run(main())
