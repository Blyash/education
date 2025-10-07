from fastapi import APIRouter, HTTPException

from ..models.auth import TokenResponse, UserCreate, UserLogin, UserProfile
from ..services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserProfile)
def register(payload: UserCreate) -> UserProfile:
    try:
        return auth.register_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin) -> TokenResponse:
    token = auth.authenticate(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    return token


@router.get("/me", response_model=UserProfile)
def get_me(authorization: str) -> UserProfile:
    token = authorization.replace("Bearer ", "")
    profile = auth.get_user_by_token(token)
    if not profile:
        raise HTTPException(status_code=401, detail="Токен недействителен")
    return profile
