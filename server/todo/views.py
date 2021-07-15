from django.contrib.auth.models import User
from rest_framework.response import Response
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


class CreateTodoView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        tg_id = request.data.get('tg_id', -1)
        vk_id = request.data.get('vk_id', -1)
        user = Profile.objects.get(Q(telegram_id=tg_id) | Q(vk_id=vk_id))
        if 'title' not in request.data or request.data['title'] == '':
            return Response(status=400)
        title = request.data['title']

        Task.objects.create(owner=user, title=title, 
            isCompleted=request.data.get('isCompleted', False), 
            deadline=request.data.get('deadline', None),
            description=request.data.get('description', ""),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          # нету плохил коментариев                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   не успеещ умирещь
            priority=request.data.get('priority', "Normal"))

        return Response(status=200)


class UpdateTodoView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        tg_id = request.data.get('tg_id', -1)
        vk_id = request.data.get('vk_id', -1)
        task_id = request.data.get('task_id', -1)
        user = Profile.objects.get(Q(telegram_id=tg_id) | Q(vk_id=vk_id))
        task = Task.objects.get(id=task_id, owner=user)

        if 'title' in request.data:
            task.title = request.data['title']
        if "isCompleted" in request.data:
            task.isCompleted = request.data['isCompleted']
        if "deadline" in request.data:
            task.deadline = request.data['deadline']
        if "description" in request.data:
            task.description = request.data['description']
        if "priority" in request.data:
            task.priority = request.data['priority']
        
        task.save()
        return Response({'msg' : 'Задача удачно изменина'}, status=200) 


class RemoveTodoView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        tg_id = request.data.get('tg_id', -1)
        vk_id = request.data.get('vk_id', -1)
        task_id = request.data.get('task_id', -1)
        user = Profile.objects.get(Q(telegram_id=tg_id) | Q(vk_id=vk_id))
        Task.objects.get(id=task_id, owner=user).delete()
        return Response({'msg' : 'Задача удачно удалена'}, status=200)