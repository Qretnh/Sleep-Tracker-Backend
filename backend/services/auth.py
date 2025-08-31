import hashlib
import hmac
import os
import urllib.parse
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.connector import get_session
from backend.db.models import User

load_dotenv()


SECRET = os.getenv("BOT_TOKEN").encode()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = os.getenv("JWT_ALGO")
JWT_EXPIRE_MINUTES = os.getenv("JWT_EXPIRE_MINUTES", 1440)


def check_telegram_auth(init_data: str) -> dict:
    """Проверка подписи Telegram initData"""
    parsed = urllib.parse.parse_qs(init_data, keep_blank_values=True)
    data_check_arr = []
    for key, value in parsed.items():
        if key == "hash":
            continue
        data_check_arr.append(f"{key}={value[0]}")
    data_check_arr.sort()
    data_check_string = "\n".join(data_check_arr)

    hash_hex = parsed["hash"][0]
    secret_key = hmac.new(b"WebAppData", SECRET, hashlib.sha256).digest()
    h = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if h != hash_hex:
        raise HTTPException(status_code=401, detail="Invalid initData")

    return {key: value[0] for key, value in parsed.items()}


def create_jwt(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


auth_scheme = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: AsyncSession = Depends(get_session),
):
    payload = decode_jwt(creds.credentials)
    user_id = payload.get("sub")
    user = await session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
