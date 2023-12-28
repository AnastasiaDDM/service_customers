'''Модуль для описания схем представления данных клиентов.'''
import datetime
import re
# import typing
from typing import Dict, Literal, Optional

from ninja import Field, ModelSchema, Schema
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
    '''Схема OUT для клиента.'''

    id: int
    phone: PhoneOut
    firstname: str | None = Field(None, max_length=name_max_length, alias='firstname.name')
    lastname: str | None = Field(None, max_length=name_max_length, alias='lastname.name')
    email: str | None = Field(None, max_length=254)  # Для пропуска email с точкой и др.
    birthday: datetime.date | None


class PhoneStrIn(Schema):
    '''Схема IN для строки телефона.'''

    phone: str

    _normalize_phone = validator('phone', allow_reuse=True)(_check_phone)


class CustomerUpdate(Schema):
    '''Схема IN Update для клиента.'''

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
    '''Схема IN для клиента. Наследует поля и валидаторы из PhoneStrIn и CustomerUpdate.'''

    pass


class CustomerResponseOut(Schema):
    '''Схема OUT для общих ответов клиента.'''

    success: bool
    message: str | None
    data: Optional[Dict] = None
