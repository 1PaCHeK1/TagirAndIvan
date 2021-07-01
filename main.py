import regex
#from auth import 
import requests
import json
import telebot
import uuid
import hashlib
from telebot import types
import re
from auth import add_user, check_user, User
from datetime import datetime

# досвидания
# Привет, я ИВаня мне 10 лет
# f"Привет, я {name} мне {age} лет"
bot = telebot.TeleBot("1837819469:AAEv8DK1M3xa0kgZn1mmRJuMb99c8M4IvrI")

cache = {}
	# cache.setdefault(request.from_user.id, {})['username'] = request.text

@bot.message_handler(commands=['start'])
def start(request):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	button1 = types.KeyboardButton("Авторизоваться")
	button2 = types.KeyboardButton("Зарегистрироваться")
	markup.add(button1)
	markup.add(button2)
	
	msg = bot.send_message(request.chat.id, "Привет, ты хочешь авторизоваться или зарегистрироваться?", reply_markup=markup)
	return	bot.register_next_step_handler(msg, Login)

def Login(request):
	if request.text == "Авторизоваться":
		cache.setdefault(request.from_user.id, {})['id'] = request.from_user.id		
		msg = bot.send_message(request.chat.id, 
			"Введите логин")
		return	bot.register_next_step_handler(msg, Auth)
	elif request.text == "Зарегистрироваться":
		cache.setdefault(request.from_user.id, {})['id'] =request.from_user.id
		msg = bot.send_message(request.chat.id, 
			"Придумайте логин")
		return	bot.register_next_step_handler(msg, Registration)
	else:
		return bot.send_message(request.chat.id, 
			"Я тебя не понял. Что ты несешь???")

def Auth(request):
	if request.from_user.id in cache and 'username' in cache[request.from_user.id]:
		msg = ""
		cache[request.from_user.id]['password'] = request.text
		if check_user(cache[request.from_user.id]['username'], cache[request.from_user.id]['password']):
			msg = "Вы вошли в учетную запись!"
		else:
			msg = "Логин или пароль не верный!"
		del cache[request.from_user.id]
		return bot.send_message(request.chat.id, msg)
	elif request.from_user.id in cache and 'id' in cache[request.from_user.id]:
		cache[request.from_user.id]['username'] = request.text
		msg = bot.send_message(request.chat.id, 
			"Введите свой пароль")
		return	bot.register_next_step_handler(msg, Auth)

def Registration(request):
	if request.from_user.id in cache and 'password' in cache[request.from_user.id]:
		cache[request.from_user.id]['email'] = request.text
		user = User(**cache[request.from_user.id]) 
		add_user(user)
		del cache[request.from_user.id]
		return bot.send_message(request.chat.id, 
			"Вы успешно зарегистрировались!")
	elif request.from_user.id in cache and 'username' in cache[request.from_user.id]:
		cache[request.from_user.id]['password'] = request.text
		msg = bot.send_message(request.chat.id, 
			"Напишите свой email")
	elif request.from_user.id in cache and 'id' in cache[request.from_user.id]:
		cache[request.from_user.id]['username'] = request.text
		msg = bot.send_message(request.chat.id, 
			"Придумайте пароль")
	return	bot.register_next_step_handler(msg, Registration)

@bot.message_handler(commands=['help'])
def hello(request):
    return bot.send_message(request.chat.id, 
        "Я умею:\n1) Говорить погоду\n2) Выступать в роли калькулятора")

@bot.message_handler(content_types=['photo', 'document', 'video'])
def upload(request):
	if request.photo is not None:
		file_id = request.photo[-1].file_id
		save_file(file_id)
	elif request.document is not None:
		file_id = request.document.file_id
		save_file(file_id)
	elif request.video is not None:
		file_id = request.video.file_id
		save_file(file_id)

	return bot.send_message(request.chat.id, "Я сохранил твой файл!")

def save_file(file_id):
	filepath = r"upload/"
	file_info = bot.get_file(file_id)
	file_type = re.findall(r"\.([\w]+)$", file_info.file_path)[0]
	file_name = str(datetime.now().strftime("%Y %m %d %H %M %S %f"))
	file = bot.download_file(file_info.file_path)
	with open(filepath + file_name + '.' + file_type, 'wb') as f:
		f.write(file)

def hash_password(password):
    salt = "3kh4gubfyneio2934jn8!@#YRfbdjhdgrhn784rrgg78cbh74eyfrtg74j58cv8ejskesd4hy8yvnomxzso2dny7ihngt5xd8ur4930yn6+9484e0\4ee0ym7ebbt9yvcm40xsy34cv5rtlkyj6/97MR%)&Jyph/6vkgyhukp876DER63785T9DNBm,';n5/'"
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
	# 55v4truibgnjiruifxkjvbgfjkji289367cf(t)

@bot.message_handler(content_types=['text'])
def message(request):
	return bot.send_message(request.chat.id, "Я тебя не понимаю")

@bot.message_handler(content_types=['sticker'])
def message(request):
    return bot.send_message(request.chat.id, "Вау классный стикер")

bot.polling()