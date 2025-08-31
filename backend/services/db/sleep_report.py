import os
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.db.sleep_log import get_sleep_logs
from backend.services.db.user import get_user
from backend.services.openai_client import openai_client

router = APIRouter()


def format_sleep_logs(reports):
    text = ""
    for report in reports:
        text += (
            f"дата: {report.date}\n"
            f"время засыпания: {report.bedtime}\n"
            f"время пробуждения: {report.wake_time}\n"
            f"уровень энергии: {report.energy}\n"
            f"качество сна: {report.sleep_quality}\n"
            f"описание: {report.feeling}\n\n"
        )
    return text


async def generate_report(
    session: AsyncSession,
    user_id: int,
    min_words: int,
    max_words: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> str:
    user = await get_user(session, user_id)
    if not user:
        return "Пользователь не найден"

    sleep_logs = await get_sleep_logs(session, user.id, start_date, end_date)
    logs_text = format_sleep_logs(sleep_logs)

    client = openai_client.get()

    chat_completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL_NAME"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты - слипмейт, помощник в деле сна и хорошего самочувствия. "
                    f"Составь отчёт на {min_words}-{max_words} слов по сну человека за последние дни."
                    f"Отметь в отчёте удачные и неудачные моменты. Можешь что-то рассказать о сне."
                    "Тон дружелюбный, можно добавить лёгкий юмор. Не будь формальным. не делай долгих введений, "
                    "будь как друг-специалист по сну. Не делай вступление, оглавление и старайся использовать "
                    "меньше неупорядоченных списков. ИЗБЕГАЙ h1 и h2 заголовков (h3 и далее можно)"
                    "Объясни закономерности, дай рекомендации. Верни отчёт в формате MarkDown."
                    "Напиши отчёт для:"
                    f"Имя: {user.name}. "
                    f"Возраст: {user.age}. "
                    f"Чем занимаюсь: {user.about}. "
                    f"Особенности: {user.notes}. "
                    f"Данные сна:\n{logs_text}"
                ),
            },
        ],
    )

    return chat_completion
