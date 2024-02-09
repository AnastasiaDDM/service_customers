'''Модуль для описания схем представления данных клиентов.'''
from datetime import datetime, date
import re
from typing import Dict, List, Literal, Optional

from django.db.models import Q
from ninja import Field, FilterSchema, Schema
from pydantic import EmailStr, validator

name_max_length = 50
gender_mask = Literal['m', 'f']
platform_mask = Literal['site', 'mobile', 'app']


def _check_phone(phone_raw: str) -> str:
    '''Метод валидации номера телефона.'''
    if phone_raw.isdigit() and len(phone_raw) == 11:
        if phone_raw[0] == '8':
            phone_raw = '7' + phone_raw[1:]
        return phone_raw
    raise ValueError('Неверный формат номера. Телефон должен состоять из 11 цифр')


def _check_name(name: str) -> str:
    '''Метод валидации name.'''
    # Строка не содержит цифр
    if re.search(r'\d+', name) is None:
        return name.title()
    raise ValueError('В имени не может быть цифр')


class PhoneStrIn(Schema):
    '''Схема IN для строки телефона.'''

    phone: str

    _normalize_phone = validator('phone', allow_reuse=True)(_check_phone)


class CustomerOut(Schema):
    '''Схема OUT для пользователя.'''

    id: int
    email: str | None = Field(None, max_length=254)  # Для пропуска email с точкой и др.
    phone: str | None
    firstname: str | None = Field(None, max_length=name_max_length, alias='firstname.name')
    lastname: str | None = Field(None, max_length=name_max_length, alias='lastname.name')
    created_at: datetime | None
    deleted_at: datetime | None
    last_auth_at: datetime | None


class CustomerOutExtended(CustomerOut):
    '''Схема OUT расширенная для пользователя. Наследует поля из CustomerOut.'''

    birthday: date | None
    gender: Optional[gender_mask] | None
    city_id: int | None
    updated_at: datetime | None
    last_auth_platform: platform_mask | None = Field(None, alias='last_auth_platform.name')
    favorites: Dict | None
    basket: Dict | None


class _CustomerIn(Schema):
    '''Схема IN для пользователя. Наследует поля и валидаторы из PhoneStrIn.'''

    firstname: str = Field(None, max_length=name_max_length)
    lastname: str = Field(None, max_length=name_max_length)
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    gender: Optional[gender_mask] = None
    city_id: Optional[int] = None

    _normalize_firstname = validator('firstname', allow_reuse=True)(_check_name)
    _normalize_lastname = validator('lastname', allow_reuse=True)(_check_name)


class CustomerIn(PhoneStrIn, _CustomerIn):
    '''Схема IN для пользователя. Наследует поля и валидаторы из PhoneStrIn и _CustomerIn.'''

    pass


class CustomerUpdate(_CustomerIn):
    '''Схема IN Update для пользователя. Наследует поля и валидаторы из CustomerIn.'''

    phone: Optional[str] = None
    last_auth_at: Optional[datetime] = None
    last_auth_platform: Optional[platform_mask] = None
    basket: Optional[Dict] = None

    _normalize_phone = validator('phone', allow_reuse=True)(_check_phone)


class CustomerFilter(FilterSchema):
    '''Схема FILTER для пользователей.'''

    id__in: List[int] = Field(None, alias='id')
    phone: str = Field(None, q='phone__icontains')
    firstname: str = Field(None, q='firstname__name__icontains')
    lastname: str = Field(None, q='lastname__name__icontains')
    email: str = Field(None, q='email__icontains')
    gender: gender_mask = Field(None, alias='gender')
    city_id__in: List[int] = Field(None, alias='city_id')
    birthday_min: Optional[date] = None
    birthday_max: Optional[date] = None
    created_at_min: Optional[date] = None
    created_at_max: Optional[date] = None
    last_auth_at_min: Optional[date] = None
    last_auth_at_max: Optional[date] = None
    last_auth_platform: platform_mask = Field(None, q='last_auth_platform__name')

    def filter_birthday_min(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(birthday__gte=value)

    def filter_birthday_max(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(birthday__lte=value)

    def filter_created_at_min(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(created_at__gte=value)

    def filter_created_at_max(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(created_at__lte=value)

    def filter_last_auth_at_min(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(last_auth_at__gte=value)

    def filter_last_auth_at_max(self, value: date) -> Q:
        '''Условие фильтра для поиска.'''
        return Q(last_auth_at__lte=value)


class CustomerResponseOut(Schema):
    '''Схема OUT для общих ответов пользователя.'''

    success: bool
    message: str | None
    data: Optional[Dict] = None


class CustomerResponseOut2xx(Schema):
    '''Схема OUT для 2xx ответов пользователя.'''
    data: List
