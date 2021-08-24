import telebot

import requests
from telebot import types
from connector import bot
from settings import host
import json

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
    try:
        response = requests.post(host + 'todo/create/', data=user_data)
    except:
        return bot.send_message(request.chat.id, f"ToDo: {user_data['title']}\nНе создано!")
    else:
        if response.status_code == 201:
            return bot.send_message(request.chat.id, f"ToDo: {user_data['title']}\nУспешно создан!")
        else:
            return bot.send_message(request.chat.id, f"ToDo: {user_data['title']}\nНе создано!")

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
        return bot.send_message(request.chat.id, f"Возникла ошибка попробуйте позже!")
        
    return bot.send_message(request.chat.id, f"Аккаунт успешно создан!")

@bot.message_handler(commands=['todos'])
def get_todos(request):
    user_data = {'tg_id' : request.from_user.id}
    try:
        response = requests.get(host + 'todo/', data=user_data)
        print(json.loads(response.content), response.status_code)
        return bot.send_message(request.chat.id, f"Я посмотрел твои заметки, все хорошо!")
    except requests.exceptions.ConnectionError:
        return bot.send_message(request.chat.id, f"Возникла ошибка попробуйте позже!")

@bot.message_handler(commands=['complete'])
def complete_todo(request):
    response = requests.get(host + 'todo/', data={'tg_id' : request.from_user.id})
    data = [ (i['id'], i['title']) for i in json.loads(response.content)['data'] if i['isCompleted']]
    keyboard = types.InlineKeyboardMarkup()
    for id, title  in data:
        keyboard.add(types.InlineKeyboardButton(title, callback_data=id))
    
    return bot.send_message(request.chat.id, f"Выбери Todo которое ты уже выполнил", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data is int)
def callback_inline(call):
    print(call, call.data)