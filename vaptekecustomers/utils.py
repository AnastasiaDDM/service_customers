'''Модуль для общих методов сущностей сервиса.'''
from typing import Any, Dict, List

import pyodbc


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
