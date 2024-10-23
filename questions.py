import random
from typing import Any, Dict, Optional, List
import json
from utils import read_json

def get_tasks(amount_of_tasks: int) -> list[dict]:
    tasks = []
    with open('questions.json', 'r', encoding='UTF-8') as file:
        tasks = json.load(file)
    return


def get_random_task():
    questions = read_json('questions.json')['questions']
    random_index = random.randint(0,len(questions) - 1)
    return questions[random_index]


