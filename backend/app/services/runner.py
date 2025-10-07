import subprocess
import tempfile
from pathlib import Path
from typing import List

from ..models.tasks import CodeSubmission, TaskCheckResult, TaskDefinition

TIMEOUT_SECONDS = 2


def execute_submission(submission: CodeSubmission, task: TaskDefinition) -> List[TaskCheckResult]:
    results: List[TaskCheckResult] = []
    for test in task.tests:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "solution.py"
            tmp_path.write_text(submission.code)
            harness_path = Path(tmpdir) / "runner.py"
            if test.input_data:
                harness_path.write_text(test.input_data)
                command = ["python3", str(harness_path)]
            else:
                command = ["python3", str(tmp_path)]
            try:
                process = subprocess.run(
                    command,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SECONDS,
                )
                stdout = process.stdout
                stderr = process.stderr
                passed = stdout == test.expected_output and process.returncode == 0
                feedback = None if passed else "Проверь вывод и убедись, что он совпадает с ожидаемым."
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout or ""
                stderr = "Время выполнения превышено"
                passed = False
                feedback = "Программа выполняется слишком долго. Попробуй оптимизировать решение."
            except Exception as exc:  # pragma: no cover - защитный контур
                stdout = ""
                stderr = str(exc)
                passed = False
                feedback = "Во время запуска произошла ошибка."
            results.append(
                TaskCheckResult(
                    passed=passed,
                    stdout=stdout or "",
                    stderr=stderr or "",
                    feedback=feedback,
                )
            )
    return results
