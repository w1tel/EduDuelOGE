import json

def renumber_tasks():
    # Читаем JSON файл
    with open('database/questions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Функция для рекурсивной нумерации заданий
    def renumber_recursive(items, counter=1):
        for item in items:
            # Если это вложенный массив tasks
            if isinstance(item, dict) and "tasks" in item:
                counter = renumber_recursive(item["tasks"], counter)
            # Если это задание
            elif isinstance(item, dict) and "taskType" in item:
                item["sequenceNumber"] = counter
                counter += 1
        return counter

    # Запускаем нумерацию
    renumber_recursive(data["tasks"])

    # Записываем обновленный JSON файл
    with open('database/questions.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    try:
        renumber_tasks()
        print("Нумерация заданий успешно обновлена")
    except Exception as e:
        print(f"Произошла ошибка: {e}") 