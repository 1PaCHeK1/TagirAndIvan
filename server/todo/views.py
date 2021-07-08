from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Q

from .models import Task
from .serializers import TaskSerializer, TaskShortSerializer
from server.models import Profile


class GetAllTodo(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        tg_id = request.data.get('tg_id', -1)
        vk_id = request.data.get('vk_id', -1)

        user = Profile.objects.get(Q(telegram_id=tg_id) | Q(vk_id=vk_id))
        todos = Task.objects.filter(owner=user)
        return Response({'data': TaskSerializer(todos, many=True).data}, status=200)

    def post(self, request):
        pass

class CreateTodoView(APIView):
    pass

class UpdateTodoView(APIView):
    pass

class RemoveTodoView(APIView):
    pass