from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_markup_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Пройти тест", callback_data="cb_test"),
        InlineKeyboardButton("Мой рейтинг", callback_data="cb_stats"),
        InlineKeyboardButton("Настройки", callback_data="cb_setting"),
    )
    return markup


def get_markup_test_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Случайный", callback_data="cb_random"),
        InlineKeyboardButton("Серия", callback_data="cb_series"),
        InlineKeyboardButton("Назад", callback_data="cb_back"),
    )

    return markup


def get_markup_back_button():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="cb_back"))

    return markup


def get_markup_settings_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "Количество вопросов в серии", callback_data="cb_number_of_tests"
        ),
        InlineKeyboardButton("Назад", callback_data="cb_back"),
    )
    return markup

def get_markup_solution_button(mode: str):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Решение", callback_data="cb_solution"))
    if mode == "seria_questions":
        markup.add(InlineKeyboardButton("Следующий вопрос ➡️", callback_data="cb_next"))
    else:
        markup.add(InlineKeyboardButton("В главное меню 🏠", callback_data="cb_back"))
        
    return markup


def get_markup_next_button():
    markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton("Дальше →", callback_data="cb_next")
    markup.add(next_button)
    return markup