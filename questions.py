import random
from typing import Any, Dict, Optional, List
import json
import os
from utils import read_json, write_json

def get_tasks(amount_of_tasks) -> list[dict, ...]:
    """Читает задачи из файла и возвращает нужное их количество"""
    return


def get_random_task():
    questions = read_json('questions.json')['questions']
    random_index = random.randint(0,len(questions) - 1)
    return questions[random_index]


