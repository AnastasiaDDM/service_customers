'''Модуль для описания сущности Обратной связи от пользователей сайта.'''
from django.db import models

from customers.models import Customers, Platforms


class Feedback(models.Model):
    '''Модель для обратной связи от пользователей сайта.'''

    url = models.URLField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    comment = models.CharField()
    platform = models.ForeignKey(
        Platforms,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    customer = models.ForeignKey(
        Customers,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        ordering = ['-created_at']
