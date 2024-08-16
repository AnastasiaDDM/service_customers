'''Модуль для методов API по работе с сущностью Клиента.'''
from typing import Any, Dict, List, Union

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Query, Router
from ninja.pagination import LimitOffsetPagination, paginate

from .models import Customers, Firstnames, Lastnames, Phones
from .schemas import (
    CustomerFilter, CustomerIn, CustomerOut, CustomerOutExtended, CustomerResponseOut,
    CustomerUpdate, PhoneStrIn
)

router = Router()


def _filling_names(data_dict: Dict[str, Any]) -> None:
    '''
    Внутренний метод заполнения ФИО пользователя (firstname, lastname).

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


@router.get('', summary='Список пользователей', response=List[CustomerOutExtended])
@paginate(LimitOffsetPagination)
def list_customers(request: HttpRequest, filters: CustomerFilter = Query(...)) -> List[Customers]:
    '''
    Метод получения списка пользователей.

    Аргументы:
        request (HttpRequest): информация о запросе.
        filters (Query): фильтры запроса из параметров.

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
              "phone": {
                "id": 1,
                "code": "7",
                "number": "9046573823"
              },
              "firstname": "Иван",
              ...
            }, ...
          ],
          "count": 2
        }
    '''
    customers = filters.filter(
        Customers.objects.all().select_related('phone', 'firstname', 'lastname')
    )

    return customers


@router.post(
    '',
    summary='Создание пользователя',
    response={200: CustomerOut, 400: CustomerResponseOut}
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
          "gender": "M"
        }
        response: {
          "id": 446200,
          "phone": {
            "id": 78364,
            "code": "7",
            "number": "9041482222"
          },
          "firstname": "Иван",
          "lastname": "Иванов",
          "email": "ivanov@mail.ru",
          "birthday": "2000-12-20"
        }
    '''
    data_dict = data.dict()

    # Добавляем или получаем из базы номер
    phone, phone_created = Phones.objects.get_or_create(
        number=data_dict['phone'][-10:],
        code=data_dict['phone'][:-10]
    )
    # Телефон в базе уже существует
    if not phone_created:
        # Такой телефон уже зарегистрирован, невозможно добавить клиента
        # TODO переписать return на осмысленный
        return 400, {'success': False, 'message': 'Телефон в базе уже существует'}

    # Сначала обработаем поля внешних ключей (firstname, lastname)
    _filling_names(data_dict)

    # Получаем максимальный id из базы
    max_id = Customers.objects.values('id').order_by('-id').first()
    if not max_id:
        max_id = {'id': 0}
    # Устанавливаем значения атрибутам
    data_dict['id'] = max_id.get('id', 0) + 1
    data_dict['phone'] = phone
    data_dict['created_at'] = timezone.now()

    # Создание instance Customers
    customer = Customers()
    for attr, value in data_dict.items():
        if value:
            setattr(customer, attr, value)

    customer.save()

    return 200, customer


@router.get('{customer_id}/', summary='Просмотр пользователя', response=CustomerOut)
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
        {"id": 14722, "phone": {"id": 1, "code": "7", "number": "9025163138"},
        "firstname": "Виктор", "lastname": null, "email": "ving@mail.ru", "birthday": null}
    '''
    customer = get_object_or_404(
        Customers.objects.select_related('phone', 'firstname', 'lastname'),
        id=customer_id
    )
    return customer


@router.delete(
    '{customer_id}/',
    summary='Удаление пользователя',
    response=CustomerResponseOut
)
def delete_customer(request: HttpRequest, customer_id: int) -> Dict[str, str | bool | None]:
    '''
    Метод безвозвратного удаления пользователя.

    Аргументы:
        request (HttpRequest): информация о запросе.
        customer_id (int): id пользователя.

    Возвращаемый результат:
        (CustomerResponseOut): json ответа выполнения операции.

    Примеры:
        >>>> delete_customer(HttpRequest(), 14722)
        {'success': True, 'message': None}
    '''
    customer = get_object_or_404(Customers, id=customer_id)
    # При удалении телефона, каскадно удаляются пользователь и его избранные товары
    customer.phone.delete()
    return {'success': True, 'message': None}


@router.patch('{customer_id}/', summary='Изменение пользователя', response=CustomerOut)
def update_customer(request: HttpRequest, customer_id: int, data: CustomerUpdate) -> Customers:
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
          "lastname": "Иванов1"
        }
        response: {
          "id": 446200,
          "phone": {
            "id": 78364,
            "code": "7",
            "number": "9041482222"
          },
          "firstname": "Иван",
          "lastname": "Иванов1",
          "email": "ivanov@mail.ru",
          "birthday": "2000-12-20"
        }
    '''
    customer = get_object_or_404(Customers, id=customer_id, deleted_at=None)
    data_dict = data.dict()

    # Сначала обработаем поля внешних ключей (firstname, lastname)
    _filling_names(data_dict)

    for attr, value in data_dict.items():
        if value:
            setattr(customer, attr, value)

    customer.save()

    return customer


@router.patch(
    '{customer_id}/phone',
    summary='Изменение телефона пользователя',
    response=CustomerResponseOut
)
def update_phone(
        request: HttpRequest,
        customer_id: int,
        data: PhoneStrIn
) -> Dict[str, bool | str]:
    '''
    Метод изменения телефона пользователя.

    Аргументы:
        request (HttpRequest): информация о запросе.
        customer_id (int): id пользователя.

    Тело запроса:
        data (PhoneStrIn): данные о пользователе из запроса (телефон).

    Возвращаемый результат:
        (CustomerResponseOut): json ответа выполнения операции.

    Примеры:
        >>>> update_phone(HttpRequest(), 446200, {'phone': '79041482220'})
        {'success': True, 'message': 'Номер успешно изменен'}
    '''
    data_dict = data.dict()
    # Поиск клиента
    customer = get_object_or_404(
        Customers.objects.select_related('phone'),
        id=customer_id
    )

    # Проверить не используется ли новый номер
    count_phones = Phones.objects.filter(
        number=data_dict['phone'][-10:],
        code=data_dict['phone'][:-10]
    ).count()
    # Телефон еще не используется
    if count_phones == 0:
        # TODO валидация нового телефона
        # Валидация нового телефона
        # ...

        phone_new = Phones.objects.create(
            number=data_dict['phone'][-10:],
            code=data_dict['phone'][:-10]
        )
    else:
        return {'success': False, 'message': 'Номер уже занят'}

    phone_old = customer.phone
    # Назначить новый номер клиенту
    customer.phone = phone_new
    # Сохранить изменения
    customer.save()
    # Удалить старый номер из БД
    phone_old.delete()

    return {'success': True, 'message': 'Номер успешно изменен'}
