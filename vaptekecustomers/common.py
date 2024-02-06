'''Модуль для общих методов сущностей сервиса.'''
from typing import Any, Dict, List, Union, Optional

from django.shortcuts import get_object_or_404

import pyodbc

from customers.models import Customers, Platforms


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
    # Вместо ошибки возвращать None
    if kwargs.get('return_error', True) is False:
        try:
            return get_object_or_404(Customers, id=customer_id, deleted_at=None)
        except Exception:
            return None

    return get_object_or_404(Customers, id=customer_id, deleted_at=None)


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
