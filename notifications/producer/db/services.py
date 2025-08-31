from typing import Sequence

from db.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()
