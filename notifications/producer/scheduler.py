import asyncio
import json
import os
from datetime import datetime

import aio_pika
from db.services import get_all_users
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("NOTIFICATIONS_QUEUE")


async def send_to_queue(message: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue.name,
        )


async def scan_users_and_send_notifications(session: AsyncSession):
    now = datetime.now().strftime("%H:%M")
    users = await get_all_users(session)

    for user in users:
        if (
            user.morning_notification
            and user.morning_notification.strftime("%H:%M") == now
        ):
            await send_to_queue(
                {"telegram_id": user.telegram_id, "text": "Доброе утро!\nКак спалось?"}
            )
        if (
            user.evening_notification
            and user.evening_notification.strftime("%H:%M") == now
        ):
            await send_to_queue(
                {
                    "telegram_id": user.telegram_id,
                    "text": "Привет!😊 \nКому-то пора идти отдыхать",
                }
            )


async def scheduler_loop(session: AsyncSession):
    while True:
        await scan_users_and_send_notifications(session)
        await asyncio.sleep(60)
