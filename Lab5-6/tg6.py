import telebot
from telebot import types

bot = telebot.TeleBot('8228537187:AAHebvs5emWyFpl7zPXB0Ds7RaVo0ttWnyQ')
name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            bot.register_next_step_handler(message, get_age)
            return

    show_confirmation(message.from_user.id)


def show_confirmation(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Тебе {age} лет, тебя зовут {name} {surname}?'
    bot.send_message(chat_id, text=question, reply_markup=keyboard)


def show_change_options(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    key_name = types.InlineKeyboardButton(text='Имя', callback_data='change_name')
    key_surname = types.InlineKeyboardButton(text='Фамилия', callback_data='change_surname')
    key_age = types.InlineKeyboardButton(text='Возраст', callback_data='change_age')
    keyboard.add(key_name, key_surname, key_age)
    bot.send_message(chat_id, 'Что вы хотите поменять?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        show_change_options(call.message.chat.id)
    elif call.data.startswith('change_'):
        handle_change_request(call)


def handle_change_request(call):
    chat_id = call.message.chat.id
    change_type = call.data.split('_')[1]

    if change_type == 'name':
        bot.send_message(chat_id, 'Введите новое имя:')
        bot.register_next_step_handler(call.message, process_name_change)
    elif change_type == 'surname':
        bot.send_message(chat_id, 'Введите новую фамилию:')
        bot.register_next_step_handler(call.message, process_surname_change)
    elif change_type == 'age':
        bot.send_message(chat_id, 'Введите новый возраст:')
        bot.register_next_step_handler(call.message, process_age_change)


def process_name_change(message):
    global name
    name = message.text
    show_confirmation(message.chat.id)


def process_surname_change(message):
    global surname
    surname = message.text
    show_confirmation(message.chat.id)


def process_age_change(message):
    global age
    try:
        age = int(message.text)
        show_confirmation(message.chat.id)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, process_age_change)


bot.polling(none_stop=True, interval=0)
