'''Модуль для маршрутизации всех методов Клиента и Избранных.'''
from django.urls import path

from .api import api

urlpatterns = [
    path('', api.urls),
]
