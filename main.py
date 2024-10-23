import telebot
from dotenv import load_dotenv
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import read_json, write_json, ensure_json_file_exists, register_user, is_registered, get_user_data, update_user_data, delete_user, get_all_users
from questions import get_random_task
from constants import HELP_COMMAND_TEXT

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
  user_id = message.from_user.id
  if not is_registered(user_id):
    bot.send_message(user_id,'Мы тебя зарегестрировали👌')
    user_data = {
      'username':message.from_user.username,
      'statistic': {"total_tets":0, "correct_answers": 0},
      "number_of_tests":3,
      "state": "main_menu"
      }
    
    users[user_id] = user_data
    register_user(user_id, user_data)
  else:
    bot.send_message(user_id,'Ты уже есть в базе данных😊')
    
    
  #TODO Удалять сообщения после отправки через какое-то время 
  bot.send_message(user_id,"Привет ✌️ ")
  bot.send_message(user_id, " Я помогу тебе с сдачей экзамена. Выбери, что ты хочешь сделать:", reply_markup=get_markup_main_menu())

def get_markup_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Пройти тест", callback_data="cb_test"),
              InlineKeyboardButton("Мой рейтинг", callback_data="cb_stats"),
              InlineKeyboardButton("Настройки", callback_data="cb_setting"))
    return markup

def get_markup_test_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Случайный", callback_data="cb_random"),
              InlineKeyboardButton("Серия", callback_data="cb_series"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_test":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Пройти тест😎', reply_markup=get_markup_test_menu())
    elif call.data == 'cb_series':
        bot.answer_callback_query(call.id, "Серия")
    elif call.data == 'cb_random':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, get_random_task()['text'])``
    elif call.data == "cb_stats":
        bot.answer_callback_query(call.id, "Мой рейтинг")
        
    elif call.data == "cb_setting":
        bot.answer_callback_query(call.id, "Настройки")
    

@bot.message_handler(commands=['help'])
def help_message(message):
  bot.send_message(message.chat.id, HELP_COMMAND_TEXT, parse_mode='HTML')






bot.infinity_polling()





