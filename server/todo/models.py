from django.db import models
from server.models import Profile

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('ES', 'Easy'),
        ('NM', 'Normal'),
        ('HD', 'Hard')
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    isCompleted = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True)
    description = models.CharField(max_length=256, blank=True)
    priority = models.CharField(max_length=2, 
        choices=PRIORITY_CHOICES,
        default='NM')