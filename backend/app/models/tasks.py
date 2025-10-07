from typing import List, Optional

from pydantic import BaseModel


class CodeTestCase(BaseModel):
    input_data: Optional[str] = None
    expected_output: str


class TaskCheckResult(BaseModel):
    passed: bool
    stdout: str
    stderr: str
    feedback: Optional[str] = None


class CodeSubmission(BaseModel):
    task_id: str
    code: str


class TaskDefinition(BaseModel):
    id: str
    lesson_id: str
    title: str
    prompt: str
    starter_code: str
    tests: List[CodeTestCase]
    xp_reward: int


class SubmissionResponse(BaseModel):
    task_id: str
    passed: bool
    results: List[TaskCheckResult]
    earned_xp: int
