'''Модуль для описания сущности Клиента и вспомогательных.'''
from django.contrib.postgres.indexes import HashIndex
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

    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'lastnames'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}_{self.name}'


class Phones(models.Model):
    '''Модель для номеров телефонов.'''

    code = models.CharField(max_length=4)
    number = models.CharField(max_length=10)

    class Meta:
        db_table = 'phones'
        ordering = ['id']
        # HashIndex не используется при составных ключах
        indexes = (
            HashIndex(
                fields=('number',),
                name='number_idx',
            ),
            models.Index(fields=['number', 'code'], name='number_code_idx'),
        )

    def __str__(self) -> str:
        return f'{self.id}_{self.code}-{self.number}'


class Customers(models.Model):
    '''Модель для клиента.'''

    id = models.IntegerField('id', primary_key=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    # Удаляем номер - каскадно удаляется и клиент
    phone = models.OneToOneField(Phones, on_delete=models.CASCADE, unique=True)
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
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    last_auth_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'customers'
        ordering = ['id']
