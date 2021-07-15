from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=256)
    telegram_id = models.IntegerField(blank=True, null=True)
    vk_id = models.IntegerField(blank=True, null=True)
