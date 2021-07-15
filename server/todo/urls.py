from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', GetAllTodo.as_view()),
    path('create/', CreateTodoView.as_view()),
    path('update/', UpdateTodoView.as_view()),
    path('delete/', RemoveTodoView.as_view()),
]