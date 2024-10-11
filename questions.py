import random
from typing import Any, Dict, Optional, List
import json
import os
from utils import read_json, write_json

def start_tasks():
    random_task = get_random_task()


def get_random_task():
    questions = read_json('questions.json')['questions']
    random_index = random.randint(0,len(questions) - 1)
    return questions[random_index]


