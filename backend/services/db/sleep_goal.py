from datetime import time
from typing import Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.sleep_goal import GoalType, SleepGoal


def str_to_time(s: Optional[str]) -> Optional[time]:
    if not s:
        return None
    h, m = map(int, s.split(":"))
    return time(hour=h, minute=m)


async def add_goal(
    session: AsyncSession,
    user_id: int,
    goal_type: GoalType,
    value_time: Optional[str] = None,
    value_hours: Optional[int] = None,
) -> SleepGoal:
    new_goal = SleepGoal(
        user_id=user_id,
        goal_type=goal_type,
        value_time=str_to_time(value_time),
        value_hours=value_hours,
    )
    session.add(new_goal)
    await session.commit()
    await session.refresh(new_goal)
    return new_goal


async def delete_goal(session: AsyncSession, goal_id: int) -> bool:
    result = await session.execute(
        delete(SleepGoal).where(SleepGoal.id == goal_id)
    )
    await session.commit()
    return result.rowcount > 0  # вернёт True, если что-то реально удалилось


async def get_user_goals(
    session: AsyncSession, user_id: int
) -> Sequence[SleepGoal]:
    result = await session.execute(
        select(SleepGoal).where(SleepGoal.user_id == user_id)
    )
    return result.scalars().all()
