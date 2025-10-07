from datetime import datetime
from typing import Dict, List

from ..models.course import LessonProgress

_PROGRESS: Dict[str, Dict[str, LessonProgress]] = {}


def get_progress(user_id: str) -> List[LessonProgress]:
    return list(_PROGRESS.get(user_id, {}).values())


def update_progress(user_id: str, lesson_id: str, completed: bool, score: int) -> LessonProgress:
    lesson_progress = _PROGRESS.setdefault(user_id, {}).get(lesson_id)
    if not lesson_progress:
        lesson_progress = LessonProgress(
            lesson_id=lesson_id,
            completed=False,
            completed_at=None,
            attempts=0,
            best_score=None,
        )

    lesson_progress.attempts += 1
    if completed:
        lesson_progress.completed = True
        lesson_progress.completed_at = datetime.utcnow()
        if lesson_progress.best_score is None or score > lesson_progress.best_score:
            lesson_progress.best_score = score

    _PROGRESS[user_id][lesson_id] = lesson_progress
    return lesson_progress
