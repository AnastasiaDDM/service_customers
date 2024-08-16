'''Модуль для описания схем представления данных клиентов.'''
import datetime
import re
from typing import Dict, List, Literal, Optional

from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema, Schema
from pydantic import EmailStr, validator

from .models import Phones

name_max_length = 50


def _check_phone(phone_raw: str) -> str:
    '''Метод валидации номера телефона.'''
    if phone_raw.isdigit() and 11 <= len(phone_raw) <= 14:
        if phone_raw[0] == '8' and len(phone_raw) == 11:
            phone_raw = '7' + phone_raw[1:]
        return phone_raw
    raise ValueError('Неверный формат номера. Телефон должен состоять из 11-14 цифр')


def _check_name(name: str) -> str:
    '''Метод валидации name.'''
    # Строка не содержит цифр
    if re.search(r'\d+', name) is None:
        return name.title()
    raise ValueError('В имени не может быть цифр')


class PhoneOut(ModelSchema):
    '''Схема OUT для телефона.'''

    code: str = Field(pattern=r'^\d{1,4}$')
    number: str = Field(pattern=r'^\d{10}$')

    class Config:
        model = Phones
        model_fields = ['id', 'code', 'number']


class CustomerOut(Schema):
    '''Схема OUT для пользователя.'''

    id: int
    phone: PhoneOut
    firstname: str | None = Field(None, max_length=name_max_length, alias='firstname.name')
    lastname: str | None = Field(None, max_length=name_max_length, alias='lastname.name')
    email: str | None = Field(None, max_length=254)  # Для пропуска email с точкой и др.
    birthday: datetime.date | None


class CustomerOutExtended(CustomerOut):
    '''Схема OUT расширенная для пользователя. Наследует поля из CustomerOut.'''

    gender: Optional[Literal['M', 'F']] | None
    city_id: int | None
    created_at: datetime.datetime | None
    last_auth_at: datetime.datetime | None


class PhoneStrIn(Schema):
    '''Схема IN для строки телефона.'''

    phone: str

    _normalize_phone = validator('phone', allow_reuse=True)(_check_phone)


class CustomerUpdate(Schema):
    '''Схема IN Update для пользователя.'''

    firstname: str = Field(None, max_length=name_max_length)
    lastname: str = Field(None, max_length=name_max_length)
    email: Optional[EmailStr] = None
    birthday: Optional[datetime.date] = None
    gender: Optional[Literal['M', 'F']] = None
    city_id: Optional[int] = None
    last_auth_at: Optional[datetime.datetime] = None

    _normalize_firstname = validator('firstname', allow_reuse=True)(_check_name)
    _normalize_lastname = validator('lastname', allow_reuse=True)(_check_name)


class CustomerIn(PhoneStrIn, CustomerUpdate):
    '''Схема IN для пользователя. Наследует поля и валидаторы из PhoneStrIn и CustomerUpdate.'''

    pass


class CustomerFilter(FilterSchema):
    '''Схема FILTER для пользователей.'''

    id__in: List[int] = Field(None, alias='id')
    gender: Literal['M', 'F'] = Field(None, alias='gender')
    city_id__in: List[int] = Field(None, alias='city_id')
    phone: str = Field(None, q='phone__number__icontains')
    firstname: str = Field(None, q='firstname__name__icontains')
    lastname: str = Field(None, q='lastname__name__icontains')
    email: str = Field(None, q='email__icontains')
    birthday_min: Optional[datetime.date] = None
    birthday_max: Optional[datetime.date] = None
    created_at_min: Optional[datetime.date] = None
    created_at_max: Optional[datetime.date] = None
    last_auth_at_min: Optional[datetime.date] = None
    last_auth_at_max: Optional[datetime.date] = None

    def filter_birthday_min(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(birthday__gte=value)

    def filter_birthday_max(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(birthday__lte=value)

    def filter_created_at_min(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(created_at__gte=value)

    def filter_created_at_max(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(created_at__lte=value)

    def filter_last_auth_at_min(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(last_auth_at__gte=value)

    def filter_last_auth_at_max(self, value: datetime.date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(last_auth_at__lte=value)


class CustomerResponseOut(Schema):
    '''Схема OUT для общих ответов пользователя.'''

    success: bool
    message: str | None
    data: Optional[Dict] = None
