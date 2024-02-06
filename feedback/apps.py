'''Приложение по работе с сущностью Обратной связи от пользователей сайта.'''
from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    '''Класс конфигураций для приложения Обратной связи от пользователей сайта.'''

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'
