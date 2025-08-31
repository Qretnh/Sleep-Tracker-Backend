import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

import backend.services.auth as JWT
from backend.core.logger import logger
from backend.db.connector import get_session
from backend.db.models.user import User
from backend.schemas.user import UserCreate, UserRead, UserUpdate
from backend.services.auth import (
    JWT_EXPIRE_MINUTES,
    check_telegram_auth,
    create_jwt,
)
from backend.services.db.user import add_new_user, get_user, update_user_info
from backend.services.verify import verify_user_owner

router = APIRouter()


@router.post("/register_user")
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    logger.info(f"Создание нового пользователя {user_in.telegram_id}")
    user_data = user_in.dict()
    user_data["id"] = user_data["telegram_id"]
    db_user = User(**user_data)
    user = await add_new_user(session, db_user)
    logger.info(f"Пользователь {user_in.telegram_id} успешно создан")

    token = create_jwt({"sub": str(user.id)})
    logger.info(f"JWT создан для пользователя {user.id}")

    return {
        "user": {
            "id": user.id,
            "name": user.name,
        },
        "access_token": token,
        "expires_in": JWT_EXPIRE_MINUTES * 60,
    }


@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Попытка получить данные {user_id}")
    verify_user_owner(user_id, current_user)

    user = await get_user(session, user_id)
    if not user:
        logger.warning(f"Пользователь {user_id} не найден")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Пользователь {user_id} обработан")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user_endpoint(
    user_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Попытка обновления данных {user_id}")
    verify_user_owner(user_id, current_user)
    update_data = user_in.dict(exclude_unset=True)

    user = await update_user_info(session, user_id, **update_data)

    if not user:
        logger.warning(f"Пользователь {user_id} не найден")
        raise HTTPException(
            status_code=404, detail="User not found or nothing to update"
        )
    logger.info(f"Данные пользователя {user_id} успешно обновлены")
    return user


@router.post("/auth")
async def auth_telegram(
    request: Request, session: AsyncSession = Depends(get_session)
):
    body = await request.json()
    init_data = body.get("initData")

    data = check_telegram_auth(init_data)
    tg_user = json.loads(data["user"])
    telegram_id = tg_user["id"]

    logger.info(f"Аутентификация Telegram ID: {telegram_id}")

    user = await session.get(User, telegram_id)
    if not user:
        user = User(id=telegram_id, name=tg_user.get("first_name", ""))
        session.add(user)
        await session.commit()
        logger.info(f"Создан новый пользователь Telegram ID: {telegram_id}")

    token = create_jwt({"sub": str(user.id)})
    logger.info(f"JWT успешно создан для Telegram ID: {telegram_id}")

    return {
        "user": {"id": user.id, "name": user.name},
        "access_token": token,
        "expires_in": JWT_EXPIRE_MINUTES * 60,
    }
