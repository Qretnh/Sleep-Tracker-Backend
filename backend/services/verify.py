from fastapi import HTTPException

from backend.core.logger import logger
from backend.db.models import User


def verify_user_owner(user_id: int, current_user: User) -> User:
    if current_user.id != user_id:
        logger.warning(
            f"Пользователь {current_user.id} попытался получить доступ к ресурсу {user_id} — отказано"
        )
        raise HTTPException(
            status_code=403, detail="Not allowed to modify this resource"
        )

    logger.debug(
        f"Проверка владельца прошла успешно: {current_user.id} == {user_id}"
    )
    return current_user
