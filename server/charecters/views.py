from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Q
import requests
from bs4 import BeautifulSoup

# Create your views here.


class star5(APIView):
    def get(self, request):
        return Response({'msg': 'https://allstartd.fandom.com/wiki/Character_List#5_Stars'}, status=200)


class star6(APIView):
    def get(self, request):
        return Response({'msg': 'https://allstartd.fandom.com/wiki/Character_List#6_Stars'}, status=200)


class orbs(APIView):
    def get(self, request):
        return Response({'msg': 'https://allstartd.fandom.com/wiki/Orbs'}, status=200)


class slezhka(APIView):
    def get(self, request, slit):
        response = requests.get(f'https://www.roblox.com/users/{slit}/profile')

        soup = BeautifulSoup(response.content, 'lxml')

        avatar = soup.find(
            'div', class_="avatar avatar-headshot-lg card-plain profile-avatar-image")

        if avatar.find('div'):
            result = avatar.find('div')
            if result.find('span', class_='game'):
                return Response({'msg': 'In game'})
            return Response({'msg': 'Online'})
        else:
            return Response({'msg': 'Offline'})

class favoritegames(APIView):
    def get(self, request, slit):
        response = requests.get(f'https://www.roblox.com/users/{slit}/profile')

        soup = BeautifulSoup(response.content, 'lxml')

        favoritegames = soup.find(
            'ul', class_="hlist game-cards")


        games = favoritegames.find_all('li')
        game = [ i.find('div', class_='game-name-title').contents[0]  for i in games ] 

        return Response({'msg' : game})

                
