'''Модуль для описания схем представления данных обратной связи от пользователей сайта.'''
from datetime import date
from typing import List, Optional

from ninja import Field, FilterSchema, ModelSchema, Schema
from pydantic import HttpUrl

from .models import Feedback
from customers.schemas import platform_mask


class FeedbackOut(Schema):
    '''Схема OUT для обратной связи.'''

    # class Config:
    #     model = Feedback
    #     model_fields = '__all__'

    id: int
    url: HttpUrl = Field(None, description='https://vapteke.ru/')
    rating: int
    comment: str
    customer_id: Optional[int] = None
    platform: str | None = Field(None, alias='platform.name')
    created_at: Optional[date] = None


class FeedbackIn(Schema):
    '''Схема IN для обратной связи.'''

    rating: int = Field(ge=1, le=5)
    comment: str
    url: HttpUrl
    customer_id: Optional[int] = None
    platform: Optional[platform_mask] = None


class FeedbackFilter(FilterSchema):
    '''Схема FILTER для обратной связи.'''

    id: Optional[int] = None
    comment: str = Field(None, q='comment__icontains')
    rating__in: List[int] = Field(None, ge=1, le=5, alias='rating')
    created_at: Optional[date] = None
    customer_id__in: List[int] = Field(None, alias='customer_id')
    platform_id__in: List[int] = Field(None, alias='platform_id')


class FeedbackDelete(FilterSchema):
    '''Схема DELETE для обратной связи.'''

    id: int = Field(None, alias='id')
