from states import (STATE_WAITING_ANSWER, STATE_START, STATE_NUM_OF_TESTS, STATE_SERIA_QUESTIONS)
import logging
from telebot.types import Message
from inline_keyboards import (get_markup_solution_button, get_markup_main_menu)
from constants import START_MAIN_MENU_TEXT
from utils import update_user

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message) -> None:
    user_id = message.from_user.id
    user_message = message.text
    logger.info(
        f"User {user_id} (type: {type(user_id)}) sent a message: {user_message} (type: {type(user_message)})"
    )
    user = get_user(user_id)
    current_state = user["state"]
    
    if current_state == STATE_WAITING_ANSWER:
        user_answer = message.text
        if user_answer == user["correct_answer_question"]:
            bot.send_message(user_id, "Правильный ответ!")
            user["statistic"]["correct_answers"] += 1
            user["statistic"]["total_tests"] += 1
            bot.send_message(
            chat_id=message.chat.id,
            text=START_MAIN_MENU_TEXT,
            reply_markup=get_markup_main_menu(),
        )
        else:
            bot.send_message(user_id, "Увы, ответ не верный!", reply_markup=get_markup_solution_button(mode=user["state"]))
            user["statistic"]["total_tests"] += 1
        user["state"] = STATE_START

        user["correct_answer_question"] = None
        user["statistic"]["success_rate"] = int(
            (user["statistic"]["correct_answers"] / user["statistic"]["total_tests"])
            * 100
        )
        
        update_user(user_id, user)
        
    elif current_state == STATE_SERIA_QUESTIONS:
        handle_series_answer(user=user, user_id=user_id, user_answer=message.text)
    elif current_state == STATE_NUM_OF_TESTS:

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

