import telebot

import requests
from telebot import types
from connector import bot
from settings import host

@bot.message_handler(commands=['create-todo'])
def create_todo(request):
    msg = bot.send_message(request.chat.id, 'Введите название ToDo')
    return bot.register_next_step_handler(msg, 
        lambda request : create_todo_title(request, 
            {'id' : request.from_user.id})
    )

def create_todo_title(request, user_data):
    user_data['title'] = request.text
    msg = bot.send_message(request.chat.id, 'Описание Todo')
    return bot.register_next_step_handler(msg, 
        lambda request : create_todo_priority(request, 
            user_data)
    )

def create_todo_priority(request, user_data):
    user_data['description'] = request.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton("Easy"))
    markup.add(types.KeyboardButton("Normal"))
    markup.add(types.KeyboardButton("Hard"))
    msg = bot.send_message(request.chat.id, "Выставь приоритет ToDo", reply_markup=markup)
    return bot.register_next_step_handler(msg,
        lambda request : create_todo_deadline(request, 
            user_data)
    )

def create_todo_deadline(request, user_data):
    if request.text.lower().strip() in ['easy', 'normal', 'hard']:  
        user_data['priority'] = request.text
        msg = bot.send_message(request.chat.id, 'Введите DeadLine')
        return bot.register_next_step_handler(msg,
            lambda request : create_todo_complete(request, 
                user_data)
        )
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton("Easy"))
        markup.add(types.KeyboardButton("Normal"))
        markup.add(types.KeyboardButton("Hard"))
        msg = bot.send_message(request.chat.id, 'Неправильно введен приоритет! Выберите один из вариантов!', reply_markup=markup)
        return bot.register_next_step_handler(msg,
            lambda request : create_todo_deadline(request, 
                user_data)
        )

def create_todo_complete(request, user_data):
    # Добавление Todo
    print(user_data)
    return bot.send_message(request.chat.id, f"ToDo: {user_data['title']}\nУспешно создан!")

@bot.message_handler(commands=['signup'])
def registration(request):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton("Пропустить"))
    msg = bot.send_message(request.chat.id, 'Введите свой VK ID', reply_markup=markup)
    return bot.register_next_step_handler(msg, 
        lambda request : registration_vkid(request, 
            {'tg_id' : request.from_user.id})
    )

def registration_vkid(request, user_data):
    if not request.text == 'Пропустить':
        user_data['vk_id'] = request.text
    user_data['username'] = request.from_user.username
    try:
        response = requests.post(host + 'registration/', data=user_data)
        print(response.status_code, response.content)
    except requests.exceptions.ConnectionError:
        return bot.send_message(request.chat.id, f"Возникла попробуйте позже!")
        
    return bot.send_message(request.chat.id, f"Аккаунт успешно создан!")