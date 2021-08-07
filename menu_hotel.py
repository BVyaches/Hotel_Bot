import requests
import telebot
from telebot import types
from translate import Translator

config = '1812941909:AAEHziQZ8GHHJEXImg2re_-wLqrLQlG1dEo'

bot = telebot.TeleBot(config)


def hello_menu(id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Я постоялец🏠', callback_data='USER'),
        types.InlineKeyboardButton('Забронировать🏢',
                                   url='https://www.booking.com'),
        types.InlineKeyboardButton('Об отеле📖 ', callback_data='ABOUT'),
        types.InlineKeyboardButton('Как добраться🚕',
                                   url='https://yandex.ru/maps/org/litsey_4/1111858881'),
        types.InlineKeyboardButton('Получить ID', callback_data='GET_ID'),
    )
    params = {
        'text': '*Что хотите сделать?*',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }

    bot.send_message(**params, chat_id=id)


def main_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Услуги📃', callback_data='SERVICE'),
        types.InlineKeyboardButton('Прочее➕', callback_data='OTHER'),
        types.InlineKeyboardButton('Оставить отзыв✏️', callback_data='REVIEW'),
        types.InlineKeyboardButton('Связаться с администратором📱',
                                   callback_data='ADMIN'),
        types.InlineKeyboardButton('Как добраться🚕',
                                   url='https://yandex.ru/maps/org/litsey_4/1111858881'),
        types.InlineKeyboardButton('Выход', callback_data='HELLO')
    )
    params = {
        'text': '*Что хотите сделать?*',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }
    if isinstance(call, types.CallbackQuery):
        bot.edit_message_text(**params, chat_id=call.from_user.id,
                              message_id=call.message.id)
    else:
        bot.send_message(**params, chat_id=call.from_user.id)


def service_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Уборка🧹', callback_data='CLEAN'),
        types.InlineKeyboardButton('Пополнение бара🧃', callback_data='BAR'),
        types.InlineKeyboardButton('Тренажёрный зал🏋️‍♂️',
                                   callback_data='GYM'),
        types.InlineKeyboardButton('Назад🔙', callback_data='MENU')
    )
    params = {
        'text': '*Выберите услугу*',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }

    if isinstance(call, types.CallbackQuery):
        bot.edit_message_text(**params, chat_id=call.from_user.id,
                              message_id=call.message.id)
    else:
        bot.send_message(**params, chat_id=call.from_user.id)


def review_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Все классно!', callback_data='COOL'),
        types.InlineKeyboardButton('Можно лучше', callback_data='BAD'),
    )
    params = {
        'text': '*Оцените нас*',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }

    if isinstance(call, types.CallbackQuery):
        bot.edit_message_text(**params, chat_id=call.from_user.id,
                              message_id=call.message.id)
    else:
        bot.send_message(**params, chat_id=call.from_user.id)


def others_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Погода🌥', callback_data='WEATH'),
        types.InlineKeyboardButton('Предсказание🔮', callback_data='PREDICT'),
        types.InlineKeyboardButton('Шутка🎉', callback_data='JOKE'),
        types.InlineKeyboardButton('Правила поведения📜',
                                   callback_data='RULES'),
        types.InlineKeyboardButton('Назад🔙', callback_data='MENU'),
    )

    params = {
        'text': '*Что хотите сделать?*',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }

    if isinstance(call, types.CallbackQuery):
        bot.edit_message_text(**params, chat_id=call.from_user.id,
                              message_id=call.message.id)
    else:
        bot.send_message(**params, chat_id=call.from_user.id)


def back_menu(id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Назад🔙', callback_data='MENU')
    )

    params = {
        'text': 'Вернуться?',
        'reply_markup': keyboard,
        "parse_mode": 'MarkDownV2'
    }

    bot.send_message(**params, chat_id=id)


def cleaning_order(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Быстрая уборка',
                                   callback_data='FAST_CLEAN'),
        types.InlineKeyboardButton('Тщательная уборка',
                                   callback_data='DEEP_CLEAN'),
        types.InlineKeyboardButton('Назад', callback_data='SERVICE')
    )

    params = {
        'text': 'Выберите тип уборки',
        'reply_markup': keyboard,
        'parse_mode': 'MarkDownV2'
    }

    bot.send_message(**params, chat_id=call.from_user.id)


def cleaning_final(call, option):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('Да',
                                   callback_data=f'{option}_YES'),
        types.InlineKeyboardButton('Нет', callback_data='SERVICE')
    )
    params = {
        'text': 'Заказываем?',
        'reply_markup': keyboard,
        'parse_mode': 'MarkDownV2'
    }

    bot.send_message(**params, chat_id=call.from_user.id)

def what_weather(city):
    search = {
        '0': '',
        'T': '',
        'M': '',
    }
    requests_headers = {
        'Accept-Language': 'ru'
    }
    translator = Translator(from_lang="ru", to_lang="en")
    url = ("https://wttr.in/" + translator.translate(city))
    try:
        response = requests.get(url, params=search, headers=requests_headers)
        if response.status_code == 200:
            result = response.text
            print(result)
            return result
        else:
            return "ошибка на сервере"

    except requests.ConnectionError:
        return 'Произошла ошибка соединения'
