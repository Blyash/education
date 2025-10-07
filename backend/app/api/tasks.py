from fastapi import APIRouter, HTTPException

from ..data.sample_content import TASKS
from ..models.tasks import CodeSubmission, SubmissionResponse, TaskDefinition
from ..services.runner import execute_submission
from ..services import progress as progress_service
from ..services import auth as auth_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskDefinition])
def list_tasks(lesson_id: str | None = None) -> list[TaskDefinition]:
    tasks = TASKS
    if lesson_id:
        tasks = [task for task in tasks if task.lesson_id == lesson_id]
    return tasks


@router.post("/{task_id}/submit", response_model=SubmissionResponse)
def submit_code(task_id: str, submission: CodeSubmission, authorization: str | None = None):
    task = next((task for task in TASKS if task.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задание не найдено")

    if submission.task_id != task_id:
        raise HTTPException(status_code=400, detail="ID задания не совпадает")

    results = execute_submission(submission, task)
    passed = all(result.passed for result in results)
    earned_xp = task.xp_reward if passed else 0

    if authorization:
        token = authorization.replace("Bearer ", "")
        profile = auth_service.get_user_by_token(token)
        if profile:
            progress_service.update_progress(profile.user_id, task.lesson_id, passed, earned_xp)
            auth_service.add_xp(profile.user_id, earned_xp)

    return SubmissionResponse(
        task_id=task_id,
        passed=passed,
        results=results,
        earned_xp=earned_xp,
    )
