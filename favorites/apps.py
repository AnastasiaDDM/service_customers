'''Приложение по работе с сущностью Избранных товаров.'''
from django.apps import AppConfig


class FavoritesConfig(AppConfig):
    '''Класс конфигураций для приложения Избранных товаров.'''

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favorites'
