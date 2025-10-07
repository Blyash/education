from fastapi import APIRouter, HTTPException

from ..data.sample_content import LESSONS, TASKS_BY_LESSON
from ..models.course import Lesson

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/", response_model=list[Lesson])
def list_lessons(world: str | None = None) -> list[Lesson]:
    lessons = list(LESSONS.values())
    if world:
        lessons = [lesson for lesson in lessons if lesson.world == world]
    return sorted(lessons, key=lambda l: (l.level, l.id))


@router.get("/{lesson_id}", response_model=Lesson)
def get_lesson(lesson_id: str) -> Lesson:
    lesson = LESSONS.get(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    return lesson


@router.get("/{lesson_id}/tasks")
def get_lesson_tasks(lesson_id: str):
    if lesson_id not in LESSONS:
        raise HTTPException(status_code=404, detail="Урок не найден")
    return TASKS_BY_LESSON.get(lesson_id, [])
