from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import backend.services.auth as JWT
from backend.core.logger import logger
from backend.db.connector import get_session
from backend.db.models import User
from backend.services.db.sleep_report import generate_report

router = APIRouter()


@router.get("/short")
async def short_report(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    """
    Короткий отчёт: 100-150 слов
    """
    logger.info(
        f"Запрос на создание короткого отчёта от пользователя {current_user.id}"
    )
    return await generate_report(
        session, current_user.id, min_words=100, max_words=150
    )


@router.get("/long")
async def long_report(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    """
    Длинный отчёт: 400-500 слов
    """
    logger.info(
        f"Запрос на создание длинного отчёта от пользователя {current_user.id}"
    )
    return await generate_report(
        session, current_user.id, min_words=400, max_words=500
    )
