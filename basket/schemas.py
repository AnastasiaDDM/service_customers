'''Модуль для описания схем представления данных корзин.'''
import datetime
from typing import List, Optional

from ninja import Field, FilterSchema, Schema


class BasketOut(Schema):
    '''Схема OUT для корзины.'''

    id: int
    customer_id: int
    item_id: int
    created_at: Optional[datetime.datetime] = None


class BasketIn(Schema):
    '''Схема IN для корзины.'''

    customer_id: int
    item_id: int


class BasketFilter(FilterSchema):
    '''Схема FILTER для корзины.'''

    id: Optional[int] = None
    customer_id__in: List[int] = Field(None, alias='customer_id')
    item_id__in: List[int] = Field(None, alias='item_id')
    created_at: Optional[datetime.datetime] = None


class BasketDelete(FilterSchema):
    '''Схема DELETE для корзины.'''

    id__in: List[int] = Field(None, alias='id')
