from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import backend.services.auth as JWT
from backend.core.logger import logger
from backend.db.connector import get_session
from backend.db.models import User
from backend.schemas.sleep_log import SleepLogCreate, SleepLogRead
from backend.services.db.sleep_log import add_sleep_log, get_sleep_logs
from backend.services.verify import verify_user_owner

router = APIRouter()


@router.post("", response_model=SleepLogRead)
async def create_sleep_log(
    log_in: SleepLogCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(
        f"Создание новой записи о сне для пользователя {current_user.id}"
    )
    log = await add_sleep_log(
        session=session,
        user_id=current_user.id,
        bedtime=log_in.bedtime,
        wake_time=log_in.wake_time,
        sleep_quality=log_in.sleep_quality,
        feeling=log_in.feeling,
        energy=log_in.energy,
    )
    logger.info(
        f"Запись о сне для пользователя {current_user.id} успешно создана"
    )
    return log


@router.get("/{user_id}", response_model=List[SleepLogRead])
async def read_sleep_logs(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Получение логов сна для пользователя {current_user.id}")
    verify_user_owner(user_id, current_user)
    logs = await get_sleep_logs(session, user_id, start_date, end_date)
    if not logs:
        logger.warning(f"Логи для {current_user.id} не найдены")
        raise HTTPException(status_code=404, detail="No sleep logs found")
    logger.info(f"Логи для {current_user.id} успешно найдены")
    return logs
