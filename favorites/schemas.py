'''Модуль для описания схем представления данных клиентов.'''
import datetime
from typing import List, Optional

from ninja import Field, FilterSchema, Schema


class FavoriteOut(Schema):
    '''Схема OUT для избранных.'''

    id: int
    customer_id: int
    item_id: int
    created_at: Optional[datetime.datetime] = None


class FavoriteIn(Schema):
    '''Схема IN для избранных.'''

    customer_id: int
    item_id: int


class FavoriteFilter(FilterSchema):
    '''Схема FILTER для избранных.'''

    id: Optional[int] = None
    customer_id__in: List[int] = Field(None, alias='customer_id')
    item_id__in: List[int] = Field(None, alias='item_id')
    created_at: Optional[datetime.datetime] = None


class FavoriteDelete(FilterSchema):
    '''Схема DELETE для избранных.'''

    id__in: List[int] = Field(None, alias='id')
