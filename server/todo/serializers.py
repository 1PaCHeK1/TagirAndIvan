from django.db.models import fields
from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'isCompleted', 'createTime',
            'deadline', 'description', 'priority')

class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'isCompleted',
            'deadline', 'priority')