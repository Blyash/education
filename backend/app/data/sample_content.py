from typing import Dict, List

from ..models.course import Lesson, LessonBlock, PracticeTask
from ..models.tasks import TaskDefinition, CodeTestCase

LESSONS: Dict[str, Lesson] = {}
TASKS_BY_LESSON: Dict[str, List[TaskDefinition]] = {}


LESSON_PAYLOADS = [
    Lesson(
        id="lesson-1",
        world="Космопорт",
        level=1,
        title="Привет, Python!",
        description="Изучаем, как писать первую программу и работать с выводом.",
        blocks=[
            LessonBlock(
                type="story",
                title="Встречаем капитана Аду",
                content="Герой прибывает на станцию и узнаёт, что такое программа.",
            ),
            LessonBlock(
                type="example",
                title="Hello, World",
                content="print(\"Привет, Галактика!\")",
            ),
            LessonBlock(
                type="challenge",
                title="Секретный маяк",
                content="Помоги роботу отправить сигнал с помощью функции print.",
            ),
        ],
        practice_tasks=[
            PracticeTask(
                id="pt-1",
                title="Попробуй print",
                prompt="Выведи своё имя и любимую планету",
                starter_code="print('')",
                xp_reward=10,
            )
        ],
    ),
    Lesson(
        id="lesson-2",
        world="Космопорт",
        level=2,
        title="Переменные и типы",
        description="Работаем с переменными и знакомимся с числами и строками.",
        blocks=[
            LessonBlock(
                type="animation",
                title="Робот объясняет переменные",
                content="Переменная — это коробочка для хранения данных.",
            ),
            LessonBlock(
                type="interactive",
                title="Соедини тип и значение",
                content="Drag-and-drop упражнение",
            ),
        ],
        practice_tasks=[
            PracticeTask(
                id="pt-2",
                title="Приветствие",
                prompt="Запроси имя и возраст, выведи приветствие",
                starter_code="name = input(\"Имя: \")\nage = int(input(\"Возраст: \") or 0)\n",
                xp_reward=15,
            )
        ],
    ),
    Lesson(
        id="lesson-4",
        world="Космопорт",
        level=4,
        title="Циклы",
        description="Создаём повторяющиеся действия с помощью for и while.",
        blocks=[
            LessonBlock(
                type="example",
                title="Отправляем спутники",
                content="for i in range(3): print(f'Спутник {i+1}')",
            ),
            LessonBlock(
                type="quiz",
                title="Выбери правильный цикл",
                content="Какая конструкция повторит действие 5 раз?",
            ),
        ],
        practice_tasks=[
            PracticeTask(
                id="pt-4",
                title="Космическая лестница",
                prompt="Выведи лестницу из символов * высотой N.",
                starter_code="height = int(input())\n",
                xp_reward=20,
            )
        ],
    ),
]

for lesson in LESSON_PAYLOADS:
    LESSONS[lesson.id] = lesson

TASKS = [
    TaskDefinition(
        id="task-hello",
        lesson_id="lesson-1",
        title="Сигнал станции",
        prompt="Выведи строку 'Привет, Галактика!'",
        starter_code="def send_signal():\n    # напиши код здесь\n    pass\n\nif __name__ == '__main__':\n    send_signal()\n",
        tests=[
            CodeTestCase(
                expected_output="Привет, Галактика!\n",
            )
        ],
        xp_reward=25,
    ),
    TaskDefinition(
        id="task-greet",
        lesson_id="lesson-2",
        title="Поприветствуй экипаж",
        prompt="Функция greet должна возвращать приветствие с именем и возрастом",
        starter_code="def greet(name: str, age: int) -> str:\n    return ''\n",
        tests=[
            CodeTestCase(
                expected_output="Привет, Ада! Тебе 12 лет!\n",
                input_data="from solution import greet\nprint(greet('Ада', 12))\n",
            )
        ],
        xp_reward=30,
    ),
    TaskDefinition(
        id="task-steps",
        lesson_id="lesson-4",
        title="Ступени ракеты",
        prompt="Напиши функцию make_steps, которая возвращает строку из N строк с растущим числом *.",
        starter_code="def make_steps(n: int) -> str:\n    return ''\n",
        tests=[
            CodeTestCase(
                input_data="from solution import make_steps\nprint(make_steps(3))\n",
                expected_output="*\n**\n***\n\n",
            )
        ],
        xp_reward=40,
    ),
]

for task in TASKS:
    TASKS_BY_LESSON.setdefault(task.lesson_id, []).append(task)
