from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import backend.services.auth as JWT
from backend.core.logger import logger
from backend.db.connector import get_session
from backend.db.models import User
from backend.schemas.sleep_goal import SleepGoalCreate, SleepGoalRead
from backend.services.db.sleep_goal import add_goal, delete_goal, get_user_goals
from backend.services.verify import verify_user_owner

router = APIRouter()


@router.post("", response_model=SleepGoalRead)
async def create_goal(
    goal_in: SleepGoalCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(
        f"Создание новой цели {goal_in.goal_type} для пользователя {current_user.id}"
    )
    goal = await add_goal(
        session=session,
        user_id=current_user.id,
        goal_type=goal_in.goal_type,
        value_time=goal_in.value_time,
        value_hours=goal_in.value_hours,
    )
    logger.info(
        f"Цель {goal_in.goal_type} пользователя {current_user.id} успешно создана"
    )
    return goal


@router.get("/{user_id}", response_model=List[SleepGoalRead])
async def read_goals(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Поиск целей для пользователя {current_user.id}")
    verify_user_owner(user_id, current_user)
    goals = await get_user_goals(session, user_id)
    if not goals:
        logger.warning(f"цели для пользователя {current_user.id} не найдены")
        raise HTTPException(status_code=404, detail="No goals found")
    return goals


@router.delete("/{goal_id}")
async def remove_goal(
    goal_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(JWT.get_current_user),
):
    logger.info(f"Удаление цели пользователем {current_user.id}")
    user_goals = await get_user_goals(session, user_id=current_user.id)
    user_goals_ids = [goal.id for goal in user_goals]
    if goal_id not in user_goals_ids:
        logger.info(f"Цель не была найдена для {current_user.id}")
        raise HTTPException(status_code=404, detail="No such goal")

    success = await delete_goal(session, goal_id)
    if not success:
        logger.info(f"Цель не была найдена для {current_user.id}")
        raise HTTPException(status_code=404, detail="Goal not found")

    logger.info(f"Цель была удалена пользователем {current_user.id}")
    return {"detail": "Goal deleted"}
