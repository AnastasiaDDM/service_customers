'''Модуль для описания сущности Избранных товаров клиентов.'''

from customers.models import Customers
from django.db import models


class Favorites(models.Model):
    '''Модель для избранных товаров.'''

    user = models.ForeignKey(Customers, on_delete=models.PROTECT)
    item = models.IntegerField(name='item_id')
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'favorites'
        ordering = ['id']
