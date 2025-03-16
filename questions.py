import random
from utils import read_json
from models import Question


def get_task_fields(task: dict) -> Question:
    """Извлекает только нужные поля из задачи"""
    return {
        "title": task["title"],
        "statement": task["statement"],
        "question": task["question"],
        "difficulty": task["difficulty"],
        "answerFormat": task["answerFormat"],
        "correctAnswer": task["correctAnswer"],
        "sequenceNumber": task["sequenceNumber"],
        "code": task.get("code", ""),
        "solutionExplanation": task["solutionExplanation"]
    }


def get_random_tasks(amount_of_tasks: int) -> list[Question]:
    all_tasks = read_json('database/questions.json')['tasks']
    tasks = [task for task in all_tasks if "taskType" in task]
    random.shuffle(tasks)
    selected_tasks = tasks[:amount_of_tasks]
    return [get_task_fields(task) for task in selected_tasks]


def get_random_task() -> Question:
    all_tasks = read_json('database/questions.json')['tasks']
    tasks = [task for task in all_tasks if "taskType" in task]
    random_index = random.randint(0, len(tasks) - 1)
    return get_task_fields(tasks[random_index])


def get_all_tasks() -> list[Question]:
    all_tasks = read_json('database/questions.json')['tasks']
    tasks = [task for task in all_tasks if "taskType" in task]
    return [get_task_fields(task) for task in tasks]
