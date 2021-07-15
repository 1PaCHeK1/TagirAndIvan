from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView



from .models import Profile

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(status=200)

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        tg_id = data.get('tg_id', None)
        vk_id = data.get('vk_id', None)
        
        if not username:
            return Response({"message" : "Blank username"}, status=400)

        user = Profile.objects.create(username=username)
        if vk_id and vk_id not in Profile.objects.all().values('vk_id'):
            user.vk_id = vk_id
        if tg_id and tg_id not in Profile.objects.all().values('telegram_id'):
            user.telegram_id = tg_id
        user.save()

        return Response(status=201)

class UpdateProfile(APIView):
    pass

class RemoveProfile(APIView):
    pass
