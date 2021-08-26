from django.http import response
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
            {'tg_id' : request.from_user.id})
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
        data = json.loads(response.content)['data'] #list[Todo]
        result_str = '\n'.join([ f"{index+1:<3} " + todo['title'] + ' ' + ('✅' if todo['isCompleted'] else '❎')
            for index, todo in enumerate(data)])

        return bot.send_message(request.chat.id, result_str)
    except requests.exceptions.ConnectionError:
        return bot.send_message(request.chat.id, f"Возникла ошибка попробуйте позже!")
    except:
        return bot.send_message(request.chat.id, f"У вас нет Todo")

@bot.message_handler(commands=['complete'])
def complete_todo(request):
    response = requests.get(host + 'todo/', data={'tg_id' : request.from_user.id})
    data = [ (i['id'], i['title']) for i in json.loads(response.content)['data'] if not i['isCompleted']]
    keyboard = types.InlineKeyboardMarkup(row_width=len(data))
    for id, title  in data:
        keyboard.add(types.InlineKeyboardButton(title, callback_data=f'complete{id}'))
    
    return bot.send_message(request.chat.id, f"Выбери Todo которое ты уже выполнил", reply_markup=keyboard)

@bot.message_handler(commands=['delete'])
def delete_todo(request):
    response = requests.get(host + 'todo/', data={'tg_id' : request.from_user.id})
    data = [ (i['id'], i['title']) for i in json.loads(response.content)['data']]
    keyboard = types.InlineKeyboardMarkup(row_width=len(data))
    for id, title  in data:
        keyboard.add(types.InlineKeyboardButton(title, callback_data=f'delete{id}'))
    
    return bot.send_message(request.chat.id, f"Выбери Todo которое ты хочешь удалить", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'delete' in call.data)
def callback_inline(call):
    response = requests.post(host + 'todo/delete/', data={
        'tg_id' : call.from_user.id,
        'task_id' : int(call.data.replace('delete', ''))
    })

    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
        text="Todo удалён")


@bot.callback_query_handler(func=lambda call: 'complete' in call.data)
def callback_inline(call):
    response = requests.post(host + 'todo/update/', data={
        'tg_id' : call.from_user.id,
        'task_id' : int(call.data.replace('complete', '')),
        'isCompleted' : True
    })

    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
        text="Статус изменен")
