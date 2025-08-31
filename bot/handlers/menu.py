import os

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dotenv import load_dotenv

load_dotenv()
router = Router()


@router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    WEB_APP_URL = os.getenv("WEB_APP_URL")
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть SleepMate тг", web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )

    await message.answer(
        "Привет! Нажми кнопку, чтобы открыть миниаппку:",
        reply_markup=kb,
    )
