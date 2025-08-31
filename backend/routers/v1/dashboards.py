from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import backend.services.auth as JWT
from backend.core.logger import logger
from backend.db.connector import get_session
from backend.db.models import User
from backend.schemas.dashboard import SleepDurationRead
from backend.services.db.sleep_log import get_sleep_logs
from backend.services.verify import verify_user_owner

router = APIRouter()


@router.get(
    "/sleep_dashboard/{user_id}", response_model=List[SleepDurationRead]
)
async def sleep_dashboard(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Попытка запросить Дашборд для {user_id}")
    verify_user_owner(user_id, current_user)
    logger.debug(f"Верификация JWT для {user_id} пройдена")
    week_ago = datetime.now().date() - timedelta(weeks=1)
    logs = await get_sleep_logs(
        session, user_id, start_date=week_ago, end_date=datetime.now().date()
    )

    dashboard = []
    for log in logs:
        bedtime_dt = datetime.combine(log.date, log.bedtime)
        wake_dt = datetime.combine(log.date, log.wake_time)
        if wake_dt < bedtime_dt:
            wake_dt += timedelta(days=1)

        duration_hours = (wake_dt - bedtime_dt).total_seconds() / 3600
        dashboard.append(
            SleepDurationRead(
                date=log.date.isoformat(), duration_hours=duration_hours
            )
        )

    return dashboard
