from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('st5/', star5.as_view()),
    path('st6/', star6.as_view()),
    path('orbs/', orbs.as_view()),
    path('roblox_status/<str:slit>/', slezhka.as_view())
]
