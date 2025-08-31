from datetime import date as dt_date
from datetime import datetime, time
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.sleep_log import SleepLog
from backend.db.models.user import User


def str_to_time(time_str: str) -> time:
    h, m, s = map(int, time_str.split(":"))
    return time(hour=h, minute=m)


async def add_sleep_log(
    session,
    user_id,
    bedtime,
    wake_time,
    sleep_quality,
    feeling,
    energy,
    date=None,
):

    log = SleepLog(
        user_id=user_id,
        bedtime=str_to_time(bedtime),
        wake_time=str_to_time(wake_time),
        sleep_quality=sleep_quality,
        feeling=feeling,
        energy=energy,
        date=dt_date.today(),
    )

    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


async def get_sleep_logs(
    session: AsyncSession, user_id: int, start_date=None, end_date=None
) -> Sequence[SleepLog]:
    if start_date and end_date:
        stmt = (
            select(SleepLog)
            .where(User.id == user_id)
            .filter(SleepLog.date >= start_date)
            .filter(SleepLog.date <= end_date)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    else:
        stmt = (
            select(SleepLog).where(User.id == user_id).order_by(SleepLog.date)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
