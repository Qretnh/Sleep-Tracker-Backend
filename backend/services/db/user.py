from typing import List, Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.user import User

from backend.services.utils.user import format_user_notifications


async def add_new_user(session: AsyncSession, new_user: User) -> User:
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return format_user_notifications(new_user)


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return format_user_notifications(user)
    return None


async def update_user_info(
    session: AsyncSession, user_id: int, **update_data
) -> Optional[User]:
    if not update_data:
        return None

    await session.execute(
        update(User).where(User.id == user_id).values(**update_data)
    )
    await session.commit()

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return format_user_notifications(user)
    return None
