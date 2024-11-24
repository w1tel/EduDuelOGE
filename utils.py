from typing import Any, Dict, Optional, List
import json
import os


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

def register_user(user_id: int, user_data: Dict[str, Any], file_path: str = 'users.json') -> bool:
        ''' Регистрирует нового пользователя.'''
        try:
            users = read_json(file_path)
        except FileNotFoundError:
            users = {}

        if str(user_id) in users:
            print("Пользователь с данным ID уже зарегистрирован.")
            return False
        
        users[user_id] = user_data

        write_json(file_path, users)

        return True

def is_registered(user_id: int, file_path: str = 'users.json') -> bool:
    ''' Проверяет, зарегистрирован ли пользователь.'''
    try:
        users = read_json(file_path)
        return str(user_id) in users
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False
    except IOError as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return False

def get_user_data(user_id: int, file_path: str = 'users.json') -> Optional[Dict[str, Any]]:
    '''Получает данные пользователя.'''
    users = read_json(file_path)
    if user_id not in users:
        return False
    return users

def update_user_data(user_id: int, new_data: Dict[str, Any], file_path: str = 'users.json') -> bool:
    '''Обновляет данные пользователя.'''
    users = read_json(file_path)
    if user_id not in users:
        return False
    users[user_id].update(new_data)
    write_json(file_path, users)
    return True

def delete_user(user_id: int, file_path: str = 'users.json') -> bool:
    ''' Удаляет пользователя из базы данных.'''
    users = read_json(file_path)
    if user_id not in users:
        return False
    del users[user_id]
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(users, json_file, ensure_ascii=False, indent=4)

    return True

def get_all_users_data(file_path: str = 'users.json'):
    ''' Возвращает список всех пользователей.'''
    with open(file_path, 'r', encoding='utf-8') as json_file:
        users = json.load(json_file)
    return users

def convert_keys_to_numbers(users):
    converted_users = {} 
    for key, value in users.items():
        try:
            key = int(key)
            converted_users[key] = value
        except ValueError:
            print(f"Пропущен ключ: '{key}' (не является числом)")
    return converted_users

