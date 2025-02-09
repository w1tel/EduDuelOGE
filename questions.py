import random

from utils import read_json

def get_random_tasks(amount_of_tasks: int) -> list[dict]:
    all_tasks = read_json('questions.json')['questions']
    random.shuffle(all_tasks)
    random_tasks = all_tasks[:amount_of_tasks]
    return random_tasks

def get_random_task():
    questions = read_json('questions.json')['questions']
    random_index = random.randint(0,len(questions) - 1)
    return questions[random_index]

