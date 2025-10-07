from datetime import datetime, timedelta
from typing import Dict, Optional

from passlib.context import CryptContext

from ..models.auth import TokenResponse, UserCreate, UserProfile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_USERS: Dict[str, Dict] = {}
_TOKENS: Dict[str, str] = {}


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def register_user(payload: UserCreate) -> UserProfile:
    if payload.email in (user["email"] for user in _USERS.values()):
        raise ValueError("Пользователь с таким email уже существует")

    user_id = f"user-{len(_USERS) + 1}"
    record = {
        "id": user_id,
        "email": payload.email,
        "password": _hash_password(payload.password),
        "display_name": payload.display_name,
        "role": payload.role,
        "created_at": datetime.utcnow(),
        "streak": 0,
        "xp": 0,
        "current_world": "Космопорт",
        "current_level": 1,
        "avatar": None,
    }
    _USERS[user_id] = record
    return _to_profile(record)


def authenticate(email: str, password: str) -> Optional[TokenResponse]:
    for record in _USERS.values():
        if record["email"] == email and _verify_password(password, record["password"]):
            token = f"token-{len(_TOKENS) + 1}"
            expires = datetime.utcnow() + timedelta(hours=4)
            _TOKENS[token] = record["id"]
            return TokenResponse(
                access_token=token,
                user_id=record["id"],
                expires_at=expires,
            )
    return None


def get_user_by_token(token: str) -> Optional[UserProfile]:
    user_id = _TOKENS.get(token)
    if not user_id:
        return None
    record = _USERS.get(user_id)
    if not record:
        return None
    return _to_profile(record)


def add_xp(user_id: str, xp: int) -> None:
    if xp <= 0:
        return
    record = _USERS.get(user_id)
    if not record:
        return
    record["xp"] += xp


def _to_profile(record: Dict) -> UserProfile:
    return UserProfile(
        user_id=record["id"],
        email=record["email"],
        display_name=record["display_name"],
        role=record["role"],
        created_at=record["created_at"],
        streak=record["streak"],
        xp=record["xp"],
        current_world=record["current_world"],
        current_level=record["current_level"],
        avatar=record["avatar"],
    )
