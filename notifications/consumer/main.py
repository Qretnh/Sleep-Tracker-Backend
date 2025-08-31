import asyncio
import json
import os

import aio_pika
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("NOTIFICATIONS_QUEUE")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
queue_local = asyncio.Queue()


async def sender():
    while True:
        data = await queue_local.get()
        try:
            await bot.send_message(chat_id=data["telegram_id"], text=data["text"])
        except Exception as e:
            print("Ошибка отправки:", e)
        await asyncio.sleep(0.05)


async def consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        async with queue.iterator() as qiterator:
            async for message in qiterator:
                async with message.process():
                    data = json.loads(message.body.decode())
                    await queue_local.put(data)


async def main():

    await asyncio.sleep(10)
    await asyncio.gather(sender(), consumer())


asyncio.run(main())
