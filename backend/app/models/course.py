from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LessonBlock(BaseModel):
    type: str
    title: str
    content: str


class PracticeTask(BaseModel):
    id: str
    title: str
    prompt: str
    starter_code: Optional[str] = None
    solution_template: Optional[str] = None
    xp_reward: int = 10


class Lesson(BaseModel):
    id: str
    world: str
    level: int
    title: str
    description: str
    blocks: List[LessonBlock]
    practice_tasks: List[PracticeTask]


class LessonProgress(BaseModel):
    lesson_id: str
    completed: bool
    completed_at: Optional[datetime]
    attempts: int
    best_score: Optional[int]
