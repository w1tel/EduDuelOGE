import telebot
import logging
from dotenv import load_dotenv
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import read_json, write_json, ensure_json_file_exists, register_user, is_registered, get_user_data, update_user_data, delete_user, get_all_users
from questions import get_random_task
from constants import HELP_COMMAND_TEXT


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
users = {}



STATE_START = "main_menu"
STATE_WAITING_ANSWER = 1



@bot.message_handler(commands=['start'])
def start_message(message):
  user_id = message.from_user.id
  user_type = type(user_id)
  
  logger.info(f"User {user_id} (type: {user_type}) sent /start command")
  
  if not is_registered(user_id):
    logger.info(f"Registering new user: {user_id} (type: {user_type})")
    bot.send_message(user_id,'Мы тебя зарегестрировали👌')
    user_data = {
      'username':message.from_user.username,
      'statistic': {"total_tets":0, "correct_answers": 0},
      "number_of_tests":3,
      "state": STATE_START,
      'correct_answer_question': None
      }
    
    users[user_id] = user_data
    register_user(user_id, user_data)
  else:
    logger.info(f"User {user_id} (type: {user_type}) is already registered")
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
    user_id = call.from_user.id
    callback_data_type = type(call.data)
    logger.info(f"User {user_id} (type: {type(user_id)}) selected callback data: {call.data} (type: {callback_data_type})")
  
    if call.data == "cb_test":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Пройти тест😎', reply_markup=get_markup_test_menu())
    elif call.data == 'cb_series':
        bot.answer_callback_query(call.id, "Серия")
    elif call.data == 'cb_random':
        bot.answer_callback_query(call.id)
        random_question = get_random_task()
        
        question_type = type(random_question)
        logger.info(f"User {user_id} received random question: {random_question['text']} (type: {question_type})")
        
        bot.send_message(call.message.chat.id, random_question['text'])
        user_id = call.from_user.id
        users[user_id]['state'] = STATE_WAITING_ANSWER
        users[user_id]['correct_answer_question'] = random_question['correct_answer']
    elif call.data == "cb_stats":
        bot.answer_callback_query(call.id, "Мой рейтинг")
        
    elif call.data == "cb_setting":
        bot.answer_callback_query(call.id, "Настройки")
    

@bot.message_handler(commands=['help'])
def help_message(message):
  bot.send_message(message.chat.id, HELP_COMMAND_TEXT, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text
    logger.info(f"User {user_id} (type: {type(user_id)}) sent a message: {user_message} (type: {type(user_message)})")
    user_keys = list(users.keys())
    user_keys_info = ", ".join([f"{key} (type: {type(key)})" for key in user_keys])
    logger.info(f"Current keys in 'users' dictionary: {user_keys_info}")

    
    current_state = users[user_id]['state']
    if current_state == STATE_WAITING_ANSWER:
      user_answer = message.text
      if user_answer == users[user_id]['correct_answer_question']:
        bot.send_message(user_id, f'Правильный ответ!')
      else:
        bot.send_message(user_id, f'Увы, ответ не верный!')
        users[user_id]['state'] = STATE_START



bot.infinity_polling()





