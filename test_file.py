import telebot
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot("7625360021:AAEUE4kphSQZPtPF4RmUdTaXoaKKHCxHitM")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)  # Регистрируем следующий шаг

def get_name(message):
    name = message.text  # Получаем имя
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_color, name)  # Передаем имя в следующий обработчик

def get_color(message, name):
    color = message.text
    bot.send_message(message.chat.id, "Какой твой любимый цвет?")
    bot.register_next_step_handler(message, get_age, name, color)

def get_age(message, name, color):
    age = message.text  # Получаем возраст
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}! Тебе {age} лет. {color}")

bot.infinity_polling()
