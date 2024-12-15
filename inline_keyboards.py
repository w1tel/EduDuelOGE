from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
