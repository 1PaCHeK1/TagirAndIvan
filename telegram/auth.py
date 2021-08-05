import json

class User:
	username : str
	password : str
	email	 : str
	id : int

	def __init__(self, id = "", username = "", password = "", email = ""):
		self.username = username
		self.password = password
		self.email = email
		self.id = id

class UserJsonParser:

	@staticmethod
	def encode(user):
		user = {
				'username' : user.username,
				'password' : user.password,
				'email' : 	user.email,
				'id' : user.id
		}						
		return user
	
	@staticmethod
	def decode(data):
		result = []
		data = json.loads(data)
		for item in data:
			print(item)
			user = User(**item)
			result.append(user)
		return result

def get_data():		
	with open('users.json') as f:
		data = json.load(f)
		return data

def add_user(user):
	data = get_data()
	data.append(UserJsonParser.encode(user))
	with open('users.json', 'w+') as f:
		f.write(json.dumps(data))

def check_user(username, password):
	data = get_data()
	for user in data:
		if user.get('username', None) == username and \
			user.get('password', None) == password:
				return True
	return False

# user = User("Ivan228anonimus", "IVlad_121206I", "12IvanI@gmail.com", 22848)
# add_user(user)
# print(check_user("test", "IVlad_121206I"))
# print(check_user("Ivan228anonimus", "IVlad_121206I"))