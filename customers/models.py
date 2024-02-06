'''Модуль для описания сущности Клиента и вспомогательных.'''
from django.db import models


class Firstnames(models.Model):
    '''Модель для имени.'''

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'firstnames'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}_{self.name}'


class Lastnames(models.Model):
    '''Модель для фамилии.'''

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'lastnames'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}_{self.name}'


class Platforms(models.Model):
    '''Модель для платформы (десктоп, мобильная версия).'''

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'platforms'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}_{self.name}'


class Customers(models.Model):
    '''Модель для клиента.'''

    id = models.IntegerField('id', primary_key=True)
    email = models.EmailField(max_length=254, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    favorites = models.JSONField(null=True, blank=True)
    basket = models.JSONField(null=True, blank=True)
    firstname = models.ForeignKey(
        Firstnames,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lastname = models.ForeignKey(
        Lastnames,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    birthday = models.DateField(null=True, blank=True)
    # choices расходует больше памяти по сравнению с Bool
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_auth_at = models.DateTimeField(null=True, blank=True)
    last_auth_platform = models.ForeignKey(
        Platforms,
        max_length=50,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'customers'
        ordering = ['id']
