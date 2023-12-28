'''Приложение по работе со служебными операциями.'''
from django.apps import AppConfig


class ServiceConfig(AppConfig):
    '''Класс конфигураций для служебных операций.'''

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'
