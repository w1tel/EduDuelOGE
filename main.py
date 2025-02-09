import telebot
import logging
from dotenv import load_dotenv
import os
from inline_keyboards import (
    get_markup_main_menu,
    get_markup_test_menu,
    get_markup_settings_menu,
    get_markup_back_button,
)
from utils import register_user
from utils import is_registered
from utils import update_user
from utils import get_user
from utils import get_users
from questions import get_random_tasks
from questions import get_random_task
from constants import HELP_COMMAND_TEXT, START_MAIN_MENU_TEXT
from constants import RATING_TEXT_TEMPLATE
from utils import get_user_rank

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

MAX_OF_TESTS = 5
STATE_NUM_OF_TESTS = "waitting_num_of_tests"
STATE_START = "main_menu"
STATE_WAITING_ANSWER = "waitting_answer"
STATE_SERIA_QUESTIONS = "seria_questions"


@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id

    logger.info(f"User {user_id} sent /start command")

    if not is_registered(user_id):
        logger.info(f"Registering new user: {user_id})")
        bot.send_message(user_id, "Мы тебя зарегистрировали👌")
        user_data = {
            "username": message.from_user.username,
            "statistic": {"total_tests": 0, "correct_answers": 0, "success_rate": 0},
            "number_of_tests": 3,
            "state": STATE_START,
            "correct_answer_question": None,
            "seria_of_questions": [],
        }

        register_user(user_id, user_data)
    else:
        logger.info(f"User {user_id} is already registered")
        bot.send_message(user_id, "Ты уже есть в базе данных")

    # TODO Удалять сообщения после отправки через какое-то время
    bot.send_message(user_id, "Привет ✌️ \nЯ помогу тебе с сдачей экзамена.  ")
    bot.send_message(
        user_id,
        START_MAIN_MENU_TEXT,
        reply_markup=get_markup_main_menu(),
    )


def get_seria_question(user):
    if user["seria_of_questions"]:
        question = user["seria_of_questions"][0]
        text_of_question = question["text"]
        correct_answer = question["correct_answer"]
        user["correct_answer_question"] = correct_answer
        return text_of_question
    return False


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    callback_data_type = type(call.data)
    logger.info(
        f"User {user_id} (type: {type(user_id)}) selected callback data: {call.data} (type: {callback_data_type})"
    )

    if call.data == "cb_test":
        bot.answer_callback_query(call.id)

        replace_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            new_text="Пройти тест",
            reply_markup=get_markup_test_menu(),
        )
    elif call.data == "cb_series":
        number_of_tests = user["number_of_tests"]

        bot.answer_callback_query(call.id, "Серия")

        questions = get_random_tasks(number_of_tests)

        user["state"] = STATE_SERIA_QUESTIONS
        user["seria_of_questions"].clear()
        user["seria_of_questions"].extend(questions)
        update_user(user_id, user)
        # нужно выводить колличество вопросов в серии
        # bot.send_message(call.message.chat.id, f'Задача - 1/{number_of_tests}')
        # bot.send_message(call.message.chat.id, get_seria_question(user))
        ask_next_question(user=user, user_id=user_id, is_first=True)
    elif call.data == "cb_random":
        bot.answer_callback_query(call.id)
        random_question = get_random_task()

        bot.send_message(call.message.chat.id, random_question["text"])
        user["state"] = STATE_WAITING_ANSWER
        user["correct_answer_question"] = random_question["correct_answer"]

        update_user(user_id, user)
    elif call.data == "cb_stats":
        bot.answer_callback_query(call.id, "Мой рейтинг")
        replace_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            new_text=get_raiting_text(user_id),
            reply_markup=get_markup_back_button(),
        )
    elif call.data == "cb_setting":
        bot.answer_callback_query(call.id, "Настройки")
        replace_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            new_text="Настройки",
            reply_markup=get_markup_settings_menu(),
        )
    elif call.data == "cb_number_of_tests":
        bot.answer_callback_query(call.id)
        replace_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            new_text=f"Сейчас выбранно {user['number_of_tests']} вопрос(-а) серии\nНапиши, сколько вопросов ты бы хотел получать в 'Серии'",
        )
        user["state"] = STATE_NUM_OF_TESTS
        update_user(user_id, user)
    elif call.data == "cb_back":
        # Обязательно вызываем answer_callback_query, чтобы убрать "часики" у пользователя
        bot.answer_callback_query(call.id)
        replace_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            new_text=START_MAIN_MENU_TEXT,
            reply_markup=get_markup_main_menu(),
        )


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, HELP_COMMAND_TEXT, parse_mode="HTML")


# обработчик ответов пользователя(проверяет на правильность ответа)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text
    logger.info(
        f"User {user_id} (type: {type(user_id)}) sent a message: {user_message} (type: {type(user_message)})"
    )
    user = get_user(user_id)
    current_state = user["state"]
    print(current_state)
    if current_state == STATE_WAITING_ANSWER:
        user_answer = message.text
        if user_answer == user["correct_answer_question"]:
            bot.send_message(user_id, f"Правильный ответ!")
            user["statistic"]["correct_answers"] += 1
            user["statistic"]["total_tests"] += 1
        else:
            bot.send_message(user_id, f"Увы, ответ не верный!")
            user["statistic"]["total_tests"] += 1
            user["state"] = STATE_START
        user["correct_answer_question"] = None
        user["statistic"]["success_rate"] = int(
            (user["statistic"]["correct_answers"] / user["statistic"]["total_tests"])
            * 100
        )
        print(user["statistic"]["success_rate"])
        print(user["statistic"]["correct_answers"])
        print(user["statistic"]["total_tests"])
        update_user(user_id, user)
        bot.send_message(
            chat_id=message.chat.id,
            text=START_MAIN_MENU_TEXT,
            reply_markup=get_markup_main_menu(),
        )
    elif current_state == STATE_SERIA_QUESTIONS:
        handle_series_answer(user=user, user_id=user_id, user_answer=message.text)
    elif current_state == STATE_NUM_OF_TESTS:
        print(user_message)
        if user_message.isdigit():
            if int(user_message) <= MAX_OF_TESTS:
                user["number_of_tests"] = int(user_message)
                update_user(user_id, user)
                bot.reply_to(message, "Окей, уже установил😎")
                user["state"] = STATE_START
                bot.send_message(
                    chat_id=message.chat.id,
                    text=START_MAIN_MENU_TEXT,
                    reply_markup=get_markup_main_menu(),
                )
            else:
                bot.reply_to(message, "Укажите меньшее количество впросов")
        else:
            bot.reply_to(message, "Введите только число")


def ask_next_question(user: dict, user_id: int, is_first: bool):
    """
    Задаёт пользователю следующий вопрос из серии.

    Параметры:
    - is_first: True, если это вызов для самого первого вопроса
      (тогда выводим "Задача - 1/number_of_tests" без pop(0),
       ибо вопросов еще не удаляли)
    - если is_first=False, значит мы уже ответили на предыдущий
      и удалили его из списка, значит нужно вывести
      "Задача - current_num/number_of_tests" и т.п.

    Логика:
      1. Если это не первый вопрос, удаляем уже использованный (pop(0)).
      2. Если остались вопросы, берём первый из оставшихся,
         вычисляем текущий порядковый номер и отправляем.
      3. Если вопросов больше нет, завершаем серию.
    """
    total = user["number_of_tests"]

    # Шаг 1. Если это не первый вопрос, удаляем предыдущий (уже отвеченный).
    if not is_first and user["seria_of_questions"]:
        user["seria_of_questions"].pop(0)

    update_user(user_id, user)  # Сохраняем изменения

    # Шаг 2. Проверяем, остались ли ещё вопросы
    if user["seria_of_questions"]:
        # Сколько осталось вопросов
        left = len(user["seria_of_questions"])
        # Текущий индекс = total - left + 1
        current_num = total - left + 1

        bot.send_message(user_id, f"Задача - {current_num}/{total}")

        # Берем первый вопрос из массива
        question = user["seria_of_questions"][0]
        user["correct_answer_question"] = question["correct_answer"]
        update_user(user_id, user)

        # Отправляем текст вопроса
        bot.send_message(user_id, question["text"])
    else:
        # Шаг 3. Если вопросов нет, серия закончилась
        bot.send_message(user_id, "Вопросы в серии закончились.")
        user["state"] = STATE_START
        update_user(user_id, user)
        bot.send_message(
            chat_id=user_id,
            text=START_MAIN_MENU_TEXT,
            reply_markup=get_markup_main_menu(),
        )


def handle_series_answer(user: dict, user_id: int, user_answer: str):
    """
    Проверяем, правильный ли ответ, обновляем статистику,
    после чего переходим к следующему вопросу,
    либо заканчиваем серию (если вопросы закончились).
    """
    correct = user_answer == user["correct_answer_question"]

    if correct:
        bot.send_message(user_id, "Правильный ответ!")
        user["statistic"]["correct_answers"] += 1
    else:
        bot.send_message(user_id, "Увы, ответ не верный!")

    user["statistic"]["total_tests"] += 1
    user["correct_answer_question"] = None  # Сбрасываем, т.к. ответ уже дан
    user["statistic"]["success_rate"] = int(
        user["statistic"]["correct_answers"] / user["statistic"]["total_tests"] * 100
    )
    # Переходим к следующему вопросу (или заканчиваем)
    ask_next_question(user, user_id, is_first=False)


def replace_message(
    chat_id, message_id, new_text, reply_markup=None, parse_mode="HTML"
):
    """
    Сначала удаляет старое сообщение по chat_id и message_id,
    затем отправляет новое сообщение с указанным текстом и кнопками.
    """
    # Удаляем старое сообщение
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    # Отправляем новое сообщение
    sent_message = bot.send_message(
        chat_id=chat_id, text=new_text, reply_markup=reply_markup, parse_mode=parse_mode
    )
    return sent_message


def get_raiting_text(user_id):
    user = get_user(user_id)
    users = get_users()
    total_tests = user["statistic"]["total_tests"]
    correct_tests = user["statistic"]["correct_answers"]
    ranking_position = get_user_rank(users, user_id)
    total_users = len(get_users())
    percentage = (correct_tests / total_tests * 100) if total_tests > 0 else 0

    return RATING_TEXT_TEMPLATE.format(
        ranking_position, total_users, correct_tests, total_tests, round(percentage, 2)
    )


bot.infinity_polling()
