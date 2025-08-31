from typing import Any, Dict, Optional

from pydantic import BaseModel


class TelegramInitData(BaseModel):
    init_data: str


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None


class TelegramAuthData(BaseModel):
    user: TelegramUser
    auth_date: int
    hash: str
    query_id: Optional[str] = None
    chat: Optional[Dict[str, Any]] = None
    receiver: Optional[Dict[str, Any]] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    tg_user_id: int
    username: Optional[str] = None
