import requests as r
from settings import host
response = r.get(host + 'test/')

print(response.json())