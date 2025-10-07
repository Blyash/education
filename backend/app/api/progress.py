from fastapi import APIRouter, HTTPException

from ..models.course import LessonProgress
from ..services import auth as auth_service
from ..services import progress as progress_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/", response_model=list[LessonProgress])
def get_user_progress(authorization: str) -> list[LessonProgress]:
    token = authorization.replace("Bearer ", "")
    profile = auth_service.get_user_by_token(token)
    if not profile:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    return progress_service.get_progress(profile.user_id)
