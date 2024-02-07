from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Профиль 👤', callback_data='profile')
    keyboard_builder.button(text='Информация ℹ️', callback_data='info')
    keyboard_builder.button(text='Выбор предмета 📚',
                            callback_data='choose_subject')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def choose_subject_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Математика проф ♾', callback_data='math')
    keyboard_builder.button(text='Русский язык 🇷🇺', callback_data='rus')
    keyboard_builder.button(text='Информатика 👨‍💻', callback_data='inf')
    keyboard_builder.button(text='<< Назад', callback_data='back_main')
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()


def choose_type_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Полезный материал 📚',
                            callback_data='material')
    keyboard_builder.button(text='Составить вариант 📝',
                            callback_data='make_test')
    keyboard_builder.button(text='Случайный вариант 🎲',
                            callback_data='random_test')
    keyboard_builder.button(text='<< Назад', callback_data='back_main')
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()


def main_cancel_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='<< Назад', callback_data='back_main')
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()
