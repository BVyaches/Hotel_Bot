'''
TODO:
#1. Add asking a cleaner func
2. Add asking a bar func
#3. Add GitHub
4. Create server
'''

import telebot
import sqlite3
from time import sleep
from random import choice
from menu_hotel import hello_menu, main_menu, service_menu, \
    review_menu, others_menu, back_menu, what_weather, cleaning_final, \
    cleaning_order

admin_id = 504312150
admin_username = 'Vyaches_s'

database = sqlite3.connect('server.db')
cursor = database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users('
               'id INT,'
               'name TEXT,'
               'room INT'
               ')')
database.commit()

config = '1812941909:AAEHziQZ8GHHJEXImg2re_-wLqrLQlG1dEo'

bot = telebot.TeleBot(config)

wishes = ['Если думаешь - не говори', 'Секрет успешного продвижения — это '
                                      'начало', 'Всё будет хорошо',
          'День будет удачным', 'Вас ожидают перемены',
          'Сегодня как раз наступило то завтра, о котором вы беспокоились '
          'вчера']

rules = 'Правила поведения:\nНе шуметь ночью\nНе портить имущество отеля' \
        '\nОтдыхать'


@bot.message_handler(commands=['view'])
def database_view(call):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    db = []
    for value in cursor.execute('SELECT * FROM users'):
        db.append(value)
    if len(db) > 0:
        all_users = ''
        for num in range(0, len(db)):
            all_users = all_users + str(db[num])
        all_users = all_users.replace('(', '')
        all_users = all_users.replace(')', '\n')
        bot.send_message(call.from_user.id, all_users)
    else:
        bot.send_message(call.from_user.id, 'База данных пуста')


@bot.message_handler(commands=['add'])
def add_user_request(message):
    if message.from_user.username != admin_username:
        bot.send_message(message.from_user.id,
                         'Извините, но вы не являетесь администратором.')
    else:
        msg = bot.send_message(message.from_user.id,
                               'Введите данные пользователя в '
                               'формате [id , ФИО клиента, '
                               'номер комнаты]')
        bot.register_next_step_handler(msg, add_user_to_data)


def add_user_to_data(call):
    try:
        call_data = call.text.split(', ')
        database = sqlite3.connect('server.db')
        cursor = database.cursor()
        cursor.execute(f'SELECT id FROM users WHERE id = "{call_data[0]}"')
        if cursor.fetchone() is None:
            cursor.execute(
                f'INSERT INTO users VALUES '
                f'("{call_data[0]}", "{call_data[1]}", {call_data[2]})')
            database.commit()
            bot.send_message(call.from_user.id, 'Данный пользователь добавлен')
        else:
            bot.send_message(call.from_user.id,
                             'Данный пользователь уже существует')

    except IndexError:
        msg = bot.send_message(call.from_user.id,
                               'Данные введены в неверном формате')

        bot.register_next_step_handler(msg, add_user_to_data)


@bot.message_handler(commands=['del'])
def del_user_request(message):
    if message.from_user.username != admin_username:
        bot.send_message(message.from_user.id,
                         'Извините, но вы не являетесь администратором.')
    else:
        msg = bot.send_message(message.from_user.id, 'Введите id пользователя')
        bot.register_next_step_handler(msg, del_user_from_data)


def del_user_from_data(call):
    call_data = call.text
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute(f'SELECT id FROM users WHERE id = "{call_data}"')
    if cursor.fetchone() is None:
        bot.send_message(call.from_user.id,
                         'Данного пользователя не существует')
    else:
        cursor.execute(f'DELETE FROM users WHERE id = "{call_data}"')
        database.commit()
        bot.send_message(call.from_user.id, 'Данный пользователь удалён')


@bot.callback_query_handler(func=lambda call: call.data == 'GET_ID')
def get_id(call):
    bot.send_message(call.from_user.id,
                     f'Ваш ID: {call.from_user.id}.'
                     f' Скажите его администратору для дальнейшей регистрации')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в отель '
                                      f'"Малина"!\n'
                                      'Надеемся, вы получите удовольствие'
                                      ' от времени, проведённого с нами')
    hello_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'USER')
def already_user(call):
    cursor = sqlite3.connect('server.db').cursor()
    cursor.execute(
        f'SELECT id FROM users WHERE id = "{call.from_user.id}"')
    if cursor.fetchone() is None:
        bot.send_message(call.from_user.id,
                         'Извините, но вас нет среди клиентов отеля. '
                         'Обратитесь к администрации')
        hello_menu(call.from_user.id)
    else:
        main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data == 'ABOUT')
def about(call):
    bot.send_message(call.from_user.id,
                     'Отель "Малина" - это многофункциональный комплекс'
                     ' в самом центре Иннополиса, состоящий из '
                     'бизнес-отеля категории 5 звезд, конференц- и банкетных'
                     ' залов, кинозалов общей вместимостью до 2200 человек, '
                     'уютной лаунж-зоны с камином.\n На территории отеля '
                     'сосредоточено все для максимально комфортного отдыха'
                     ' и приятного времяпрепровождения гостей')
    hello_menu(call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'SERVICE')
def services(call):
    service_menu(call)


@bot.callback_query_handler(func=lambda call: call.data == "MENU")
def main(call):
    main_menu(call)


@bot.callback_query_handler(
    func=lambda call: call.data in ['GYM', 'CLEAN', 'BAR'])
def service_choose(call):
    if call.data == 'GYM':
        bot.send_message(call.from_user.id, 'Тренажёрный зал открыт 24/7 '
                                            'бесплатно для всех посетителей')
        back_menu(call.from_user.id)

    elif call.data == 'BAR':
        bot.send_message(call, 'Ваш мини-бар пополняется каждое'
                               ' утро в районе 9-10 часов, для '
                               'повторного пополнения обратитесь'
                               ' к сотруднику')
        back_menu(call.from_user.id)
    else:
        cleaning_order(call)


@bot.callback_query_handler(
    func=lambda call: call.data in ['FAST_CLEAN', 'DEEP_CLEAN'])
def cleaning_continue(call):
    if call.data == 'FAST_CLEAN':
        bot.send_message(call.from_user.id, 'описание быстрой уборки')
    else:
        bot.send_message(call.from_user.id, 'описание глубокой уборки')
    cleaning_final(call, call.data)


@bot.callback_query_handler(
    func=lambda call: call.data in ['FAST_CLEAN_YES', 'DEEP_CLEAN_YES'])
def cleaning_to_admin(call):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    room = cursor.execute(
        f'SELECT room FROM users WHERE id = {call.from_user.id}').fetchone()[0]
    if call.data == 'FAST_CLEAN_YES':
        bot.send_message(admin_id, f'Заказана быстрая уборка в комнату {room}')
        bot.send_message(call.from_user.id,
                         'Быстрая уборка в ваш номер заказана')
    else:
        bot.send_message(admin_id,
                         f'Заказана тщательная уборка в комнату {room}')
        bot.send_message(call.from_user.id,
                         'Тщательная уборка в ваш номер заказана')
    sleep(2)
    main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data == 'HELLO')
def hello(call):
    hello_menu(call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'ADMIN')
def admin(call):
    bot.send_message(call.from_user.id, 'Наш номер телефона: 89991234000\n'
                                        'Или напишите нашему сотруднику: '
                                        f'@{admin_username}')
    main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data == 'REVIEW')
def review(call):
    review_menu(call)


@bot.callback_query_handler(func=lambda call: call.data in ['COOL', 'BAD'])
def feedback(call):
    if call.data == 'COOL':
        bot.send_message(call.from_user.id, 'Спасибо, нам очень приятно!')
        main_menu(call)
    else:
        msg = bot.send_message(call.from_user.id, 'Пожалуйста, скажите,'
                                                  ' что вас не устраивает')
        bot.register_next_step_handler(msg, complaint)


def complaint(message):
    try:
        cursor = sqlite3.connect('server.db').cursor()
        username = cursor.execute(
            f'SELECT name FROM users WHERE id = '
            f'"{message.from_user.id}"').fetchone()[
            0]
        bot.send_message(admin_id, f'{username} оставил '
                                   f'отзыв: \n{message.text}')

        bot.send_message(message.from_user.id,
                         'Спасибо за отзыв, мы учтём ваши пожелания')
        main_menu(message)
    except KeyError:
        bot.send_message(message.from_user.id,
                         'Вы не авторизовались, пройдите регистрацию')
        hello_menu(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'OTHER')
def other(call):
    others_menu(call)


@bot.callback_query_handler(
    func=lambda call: call.data in ['WEATH', 'PREDICT', 'RULES'])
def other_things(call):
    if call.data == 'WEATH':
        bot.send_message(call.from_user.id, what_weather('Пермь'))
        others_menu(call)
    elif call.data == 'PREDICT':
        bot.send_message(call.from_user.id, choice(wishes))
        others_menu(call)
    elif call.data == 'RULES':
        bot.send_message(call.from_user.id, rules)
        others_menu(call)


@bot.message_handler(commands=['test'])
def test(call):
    bot.send_message(call.from_user.id, 'testing' )
    sleep(60)
    bot.send_message(call.from_user.id, 'tested')

bot.polling(none_stop=True)
