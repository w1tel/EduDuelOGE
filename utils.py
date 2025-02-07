from typing import Any, Dict, Optional, List
import json
import os

from typing import TypedDict, Dict, Optional


class Statistic(TypedDict):
    total_tests: int
    correct_answers: int
    success_rate: int

class User(TypedDict):
    username: str
    statistic: Statistic
    number_of_tests: int
    state: str
    correct_answer_question: Optional[int]
    seria_of_questions: list
    

# Основной словарь
Users = Dict[int, User]

# ========== Функции для работы с json файлами ========== НАЧАЛО
def read_json(file_path: str) -> Any:   
    ''''Читает данные из JSON-файла.
    возвращает python объект'''
    with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

def write_json(file_path: str, data: Any) -> None:
    try:
        '''Записывает данные в JSON-файл.'''
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")

def ensure_json_file_exists(file_path, default_content=None, encoding='utf-8'):
    '''Проверяет наличие JSON-файла и создает его при отсутствии.'''
    if not os.path.exists(file_path):
        if default_content is not None:
            write_json(file_path, default_content)
        else:
            write_json(file_path, {})
            
# ========== Функции для работы с json файлами ========== КОНЕЦ

# ========== Функции для работы с пользователями ========== НАЧАЛО

def register_user(user_id: int, user_data: User, file_path: str = 'users.json') -> bool:
        ''' Регистрирует нового пользователя.'''
        try:
            users = get_users(file_path)
        except FileNotFoundError:
            users = {}

        if user_id in users:
            print("Пользователь с данным ID уже зарегистрирован.")
            return False
        
        users[user_id] = user_data

        write_json(file_path, users)

        return True

def is_registered(user_id: int, file_path: str = 'users.json') -> bool:
    ''' Проверяет, зарегистрирован ли пользователь.'''
    try:
        users = get_users(file_path)
        return user_id in users
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False
    except IOError as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return False

def get_user(user_id: int, file_path: str = 'users.json') -> User:
    '''Получает данные пользователя.'''
    users = get_users(file_path)
    if user_id not in users:
        return False
    return users[user_id]

def update_user(user_id: int, new_data: User, file_path: str = 'users.json') -> bool:
    '''Обновляет данные пользователя.'''
    users = get_users(file_path)
    if user_id not in users:
        return False
    users[user_id].update(new_data)
    write_json(file_path, users)
    return True

def delete_user(user_id: int, file_path: str = 'users.json') -> bool:
    ''' Удаляет пользователя из базы данных.'''
    users = get_users(file_path)
    if user_id not in users:
        return False
    del users[user_id]
    write_json(file_path, users)

    return True

def get_users(file_path: str = 'users.json') -> Users:
    ''' Возвращает список всех пользователей.'''
    return convert_keys_to_numbers(read_json(file_path)) 

def convert_keys_to_numbers(users):
    converted_users = {} 
    for key, value in users.items():
        try:
            key = int(key)
            converted_users[key] = value
        except ValueError:
            print(f"Пропущен ключ: '{key}' (не является числом)")
    return converted_users

# ========== Функции для работы с пользователями ========== КОНЕЦ

def get_user_rank(users: Users, user_id: int) -> int:
    users_rating = []
    for key, value in users.items():
        users_rating.append([key, value['statistic']['success_rate']])




    def get_two_element(element: list) -> int: 
        return element[1]

    users_rating.sort(key=get_two_element, reverse=True)
    for i in users_rating:
        if user_id in i:
            return users_rating.index(i)+1
    return None  
