'''Модуль для общих методов сущностей сервиса.'''
from typing import Any, Dict, List, Union, Optional

from django.shortcuts import get_object_or_404

import pyodbc

from customers.models import Customers, Platforms

from django.db.models import Q


def fetch_named(cursor: pyodbc.Cursor) -> List[Dict[str, Any]]:
    '''
    Метод преобразования данных из запроса в массив dict-ов.

    Аргументы:
        cursor (pyodbc.Cursor): Курсор в БД.

    Возвращаемый результат:
        (List[Dict]): Возвращает список словарей с данными о клиентах.
    '''
    rows = cursor.fetchall()

    columns = []

    for column in cursor.description:
        columns.append(column[0])

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return result


def prepare_dict(original_dict: Dict, target_fields: List[str]) -> Dict[str, Any]:
    target_dict = {}
    for field in target_fields:
        if original_dict.get(field):
            target_dict[field] = original_dict[field]
    return target_dict


def get_customer_deleted_none(customer_id: Optional[int], **kwargs) -> Union[Customers, None, Exception]:
    '''
    Метод получения неудаленного пользователя из БД.

    Аргументы:
        customer_id (int): ID пользователя.
        **kwargs (dict): необязательные параметры поиска
            (return_error (bool) = True - при отсутствие пользователя возвращать ошибку или None).

    Возвращаемый результат:
        (Union[Customers, None, Exception]): Возвращает пользователя, None или ошибку.
    '''
    models = Customers
    # Передан список необходимых полей
    if kwargs.get('only_fields'):
        models = Customers.objects.only(*kwargs['only_fields'])


    # Вместо ошибки возвращать None
    if kwargs.get('return_error', True) is False:
        try:
            return get_object_or_404(models, id=customer_id, deleted_at=None)
        except Exception:
            return None

    # Если не найден - возвращать ошибку 404
    return get_object_or_404(models, id=customer_id, deleted_at=None)


def get_or_create_platform(platform_name: Optional[str], **kwargs) -> Union[Platforms, None]:
    '''
    Метод получения неудаленного пользователя из БД.

    Аргументы:
        customer_id (int): ID пользователя.
        **kwargs (dict): необязательные параметры поиска
            (return_error (bool) = True - при отсутствие пользователя возвращать ошибку или None).

    Возвращаемый результат:
        (Union[Customers, None, Exception]): Возвращает пользователя, None или ошибку.
    '''
    if platform_name is None:
        return None
    platform, _ = Platforms.objects.get_or_create(name=platform_name)
    return platform


def check_exists_obj_by_attribute(**kwargs):

    if kwargs:
        if Customers.objects.filter(**kwargs, _connector=Q.OR).exists():
            return True
    return False
