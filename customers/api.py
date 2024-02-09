'''Модуль для методов API по работе с сущностью Клиента.'''
from typing import Any, Dict, List, Union

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Query, Router
from ninja.pagination import LimitOffsetPagination, paginate

from .models import Customers, Firstnames, Lastnames, Platforms
from .schemas import (
    CustomerFilter, CustomerIn, CustomerOut, CustomerOutExtended, CustomerResponseOut,
    CustomerUpdate, PhoneStrIn, CustomerResponseOut2xx
)
from vaptekecustomers.common import get_customer_deleted_none, get_or_create_platform, prepare_dict, check_exists_obj_by_attribute

router = Router()


def _filling_foreign_keys(data_dict: Dict[str, Any]) -> None:
    '''
    Внутренний метод заполнения внешних ключей (firstname, lastname, last_auth_platform).

    Аргументы:
        data_dict (Dict): данные о пользователе из запроса.

    Возвращаемый результат:
        None
    '''
    # Имя
    if data_dict.get('firstname'):
        firstname, _ = Firstnames.objects.get_or_create(name=data_dict['firstname'])
        data_dict['firstname'] = firstname

    # Фамилия
    if data_dict.get('lastname'):
        lastname, _ = Lastnames.objects.get_or_create(name=data_dict['lastname'])
        data_dict['lastname'] = lastname

    # Платформа
    if data_dict.get('last_auth_platform'):
        data_dict['last_auth_platform'] = get_or_create_platform(data_dict['last_auth_platform'])


def _verification_phone(data_dict: Dict[str, Any]) -> bool:
    '''
    Внутренний метод верификации номера телефона.

    Аргументы:
        data_dict (Dict): данные о пользователе из запроса.

    Возвращаемый результат:
        bool
    '''
    # # Телефон в базе уже существует
    # if Customers.objects.filter(phone=data_dict['phone']).exists():
    #     # Такой телефон уже зарегистрирован, невозможно добавить клиента
    #     return False

    if data_dict.get('phone'):
        # TODO валидация нового телефона
        # Валидация нового телефона
        pass
    return True


@router.get('', summary='Список пользователей', response=List[CustomerOut])
@paginate(LimitOffsetPagination)
def list_customers(request: HttpRequest, filters: CustomerFilter = Query(...)) -> List[Customers]:
    '''
    Метод получения списка пользователей.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Параметры:
        limit (int): количество элементов в одном ответе.
        offset (int): смещение (страница).

    Возвращаемый результат:
        (list[dict]): список json данных о пользователях.

    Примеры:
        >>>> list_customers(HttpRequest())
        {
          "items": [
            {
              "id": 1,
              "phone": "79025163111",
              "firstname": "Иван",
              ...
            }, ...
          ],
          "count": 2
        }
    '''
    customers = filters.filter(
        Customers.objects.all().select_related('firstname', 'lastname')
    )

    return customers


@router.post(
    '',
    summary='Создание пользователя',
    response={201: CustomerResponseOut2xx, 400: CustomerResponseOut}
)
def create_customer(
        request: HttpRequest,
        data: CustomerIn
) -> Union[tuple[int, Dict[str, Any]], tuple[int, Customers]]:
    '''
    Метод создания пользователя.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Тело запроса:
        data (CustomerIn): данные о пользователе из запроса.

    Возвращаемый результат:
        (CustomerOut): json данных о пользователе.

    Примеры:
        >>>> create_customer(HttpRequest(), data)
        data: {
          "phone": "79041482222",
           "firstname": "Иван",
          "lastname": "Иванов",
          "email": "ivanov@mail.ru",
          "birthday": "2000-12-20",
          "gender": "m",
          "city_id": 0,
          "last_auth_at": "2024-01-25T08:01:19.873Z",
          "last_auth_platform": "site"
        }
        response: {
          "id": 446200,
          "phone": "79041482222",
          "firstname": "Иван",
          "lastname": "Иванов",
          "email": "ivanov@mail.ru",
          "birthday": "2000-12-20",
          "city_id": 0,
          "last_auth_at": "2024-01-25T08:01:19.873Z",
          "last_auth_platform": "site"
        }
    '''
    data_dict = data.dict()

    # Проверка уникальных полей
    filter_dict = prepare_dict(data_dict, ['phone', 'email'])

    if check_exists_obj_by_attribute(**filter_dict):
        # Поля не уникальны, такой объект уже есть в бд
        return 400, {'success': False, 'message': 'Пользователь с таким телефоном или эл. почтой уже зарегистрирован'}

    # Верификация номера телефона
    if _verification_phone(data_dict):

        # Сначала обработаем поля внешних ключей (firstname, lastname, last_auth_platform)
        _filling_foreign_keys(data_dict)

        # Получаем максимальный id из базы
        max_id = Customers.objects.values('id').order_by('-id').first()
        if not max_id:
            max_id = {'id': 0}

        # Создание instance Customers
        customer = Customers()
        for attr, value in data_dict.items():
            if value:
                setattr(customer, attr, value)

        # Устанавливаем значения атрибутам
        customer.id = max_id.get('id', 0) + 1
        customer.created_at = timezone.now()

        customer.save()

        answer = {'data': [{'id': customer.id}]}

        return 201, answer

    return 400, {'success': False, 'message': 'Пользователь с таким телефоном уже зарегистрирован'}


@router.get('{customer_id}/', summary='Просмотр пользователя', response=CustomerOutExtended)
def get_customer(request: HttpRequest, customer_id: int) -> Customers:
    '''
    Метод получения данных о пользователе.

    Аргументы:
        request (HttpRequest): информация о запросе.
        customer_id (int): id пользователя.

    Возвращаемый результат:
        (dict): json данных о пользователе.

    Примеры:
        >>>> get_customer(HttpRequest(), 14722)
        {"id": 14722, "phone": "79016606060", "firstname": "Виктор", "lastname": null, ...}
    '''
    customer = get_object_or_404(
        Customers.objects.select_related('firstname', 'lastname', 'last_auth_platform'),
        id=customer_id,
        deleted_at=None
    )

    return customer


@router.delete(
    '{customer_id}/',
    summary='Удаление пользователя',
    response={200: None, 400: None}
)
def delete_customer(request: HttpRequest, customer_id: int) -> tuple[int, None]:
    '''
    Метод удаления чувствительных данных пользователя.
    Очищаются поля email, phone, firstname_id, lastname_id.

    Аргументы:
        request (HttpRequest): информация о запросе.
        customer_id (int): id пользователя.

    Возвращаемый результат:
        (CustomerResponseOut): json ответа выполнения операции.

    Примеры:
        >>>> delete_customer(HttpRequest(), 14722)
        {'success': True, 'message': None}
    '''
    number = Customers.objects.filter(id=customer_id, deleted_at=None).update(
        deleted_at=timezone.now(),
        phone=None,
        firstname=None,
        lastname=None,
        email=None
    )

    if number:
        # Запись была изменена
        return 200, None
    return 400, None


@router.patch('{customer_id}/', summary='Изменение пользователя', response={202: None, 400: None})
def update_customer(request: HttpRequest, customer_id: int, data: CustomerUpdate) -> tuple[int, None]:
    '''
    Метод изменения пользователя.

    Аргументы:
        request (HttpRequest): информация о запросе.
        customer_id (int): id пользователя.

    Тело запроса:
        data (CustomerUpdate): данные о пользователе из запроса.

    Возвращаемый результат:
        (CustomerOut): json данных о пользователе.

    Примеры:
        >>>> update_customer(HttpRequest(), 446200, data)
        data: {
          "lastname": "Иванов новый"
        }
        response: {
          "id": 446200,
          "phone": "79041482222",
          "firstname": "Иван",
          "lastname": "Иванов новый",
          "email": "ivanov@mail.ru",
          "birthday": "2000-12-20"
        }
    '''
    customer = get_customer_deleted_none(customer_id)
    data_dict = data.dict()

    # Проверка уникальных полей
    filter_dict = prepare_dict(data_dict, ['phone', 'email'])

    if check_exists_obj_by_attribute(**filter_dict):
        # Поля не уникальны, такой объект уже есть в бд
        return 400, None

    # Верификация номера телефона
    if _verification_phone(data_dict):

        # Сначала обработаем поля внешних ключей (firstname, lastname, last_auth_platform)
        _filling_foreign_keys(data_dict)

        # Список обновляемых полей
        u_f = []
        for attr, value in data_dict.items():
            if value:
                setattr(customer, attr, value)
                u_f.append(attr)

        u_f.append('updated_at')
        customer.updated_at = timezone.now()
        customer.save(update_fields=u_f)

        return 202, None

    return 400, None
