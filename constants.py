from telebot import formatting

HELP_COMMAND_TEXT = formatting.format_text(
        formatting.hbold("/start - вызов главного меню бота") + "\n\n",

        formatting.hbold("Кнопка 'Пройти тест'"), "предлагает пройти тесты по информатике в двух режимах:\n",
        "1. ", formatting.hbold("Кнопка 'Случайный'"), " — вам выдаётся только одна случайная задача.\n",
        "2. ", formatting.hbold("Кнопка 'Серия'"), " — вам выдаётся сразу несколько случайных задач одного типа.\n\n",

        formatting.hbold("Кнопка 'Настройки'"), " позволяет изменить количество задач в режиме серии (по умолчанию 3).\n\n",

        formatting.hbold("Кнопка 'Мой рейтинг'"), " отображает ваш текущий рейтинг и достижения в тестах, позволяя вам отслеживать свой прогресс и сравнивать его с другими пользователями.",
        separator=""
    )
START_MAIN_MENU_TEXT = "Выбери, что ты хочешь сделать"

RATING_TEXT_TEMPLATE = formatting.format_text(
    "🏆 ", formatting.hbold("Твой рейтинг среди всех участников:"),
    "\n📊 ", formatting.hbold("Место:"), " #{} из #{}",
    "\n\n📈 ", formatting.hbold("Твоя статистика:"),
    "\n✅ ", formatting.hbold("Правильно решено тестов:"), " {}",
    "\n📌 ", formatting.hbold("Всего решено тестов:"), " {}",
    "\n🎯 ", formatting.hbold("Процент правильных ответов:"), " {}%",
    "\n\n💡 *Продолжай тренироваться, чтобы улучшить свой результат!*",
    separator=""
)

QUESTION_TEMPLATE = formatting.format_text(
    "📝 ", formatting.hbold("{title}"), "\n\n",
    "📚 ", formatting.hitalic("{statement}"), "\n\n",
    "❓ ", formatting.hbold("Вопрос:"), " {question}\n",
    "{code_block}",
    "📊 ", formatting.hbold("Сложность:"), " {difficulty}\n",
    "✍️ ", formatting.hbold("Формат ответа:"), " {answerFormat}",
    separator=""
)