'''Модуль для методов API по работе с сущностью Обратной связи от пользователей сайта.'''
from typing import Any, Dict, List, Union


from customers.schemas import CustomerResponseOut2xx
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Query, Router
from ninja.pagination import paginate
from ninja_extra.ordering import ordering, Ordering

from .models import Feedback
from .schemas import FeedbackOut, FeedbackIn, FeedbackFilter, FeedbackDelete, PaginationFilter #OrderingFilter
from vaptekecustomers.common import get_customer_deleted_none, get_or_create_platform

router = Router()





# def sorting_def(params_query: Dict[str, Any]):







@router.get('', summary='Список отзывов о работе сайта', response=List[FeedbackOut])
@paginate(PaginationFilter)
# @ordering(OrderingFilter)
def list_feedback(request: HttpRequest, filters: FeedbackFilter = Query(...)) -> List[FeedbackOut]:
    '''
    Метод получения списка отзывов о работе сайта.

    Аргументы:
        request (HttpRequest): информация о запросе.
        filters (Query): фильтры запроса из параметров.

    Параметры:
        limit (int): количество элементов в одном ответе.
        offset (int): смещение (страница).
        id (int): id записи.
        customer_id (list[int]): список id пользователей (в строке запроса записывается так:
                customer_id=14738&customer_id=14722)
        item_id (list[int]): список id товаров (в строке запроса записывается так:
                item_id=10&item_id=12)
        created_at (datetime): дата создания (добавления в избранные).
    Возвращаемый результат:
        (dict{"items": list[dict], "count": int}): список json данных об избранных.

    Примеры:
        >>>> list_feedback(HttpRequest())
        {
          "items": [
            {
              "id": 1,
              "customer_id": 14722,
              "item_id": 12,
              "created_at": null
            },
            {
              "id": 2,
              "customer_id": 14738,
              "item_id": 34,
              "created_at": null
            }
          ],
          "count": 2
        }
    '''
    # Отсекаем параметры для сортировки

    f = filters.dict()
    list_order = []
    list_order.append(f.pop('sort'))
    list_order.append(f.pop('sort_0'))
    list_order.append(f.pop('sort_1'))
    print(list_order)


    sorting_fields = []
    if list_order:
        # Обработка строки сортировки
        # Возможные варианты: sort=rating, sort=id:asc, sort[0]=url:asc, sort[1]=rating:desc
        for field in list_order:
            if field:
                print(field)
                list_field = field.split(':')
                if len(list_field) == 2:
                    if list_field[1] == 'desc':
                        list_field[0] = '-' + list_field[0]
                # field = list_field[0]
                sorting_fields.append(list_field[0])

    # valid_fields = [str(field.name) for field in Feedback.__dict__.keys()]
    # print(valid_fields)
    print(Feedback.__dict__.keys())
    print(list(vars(Feedback).keys()))


        # return self.remove_invalid_fields(items, fields)
    #     return fields
    # return []
    print(sorting_fields)
    print(f)

    filters = FeedbackFilter(**f)

    # sort_args, filters = sorting_def(f)

    print(filters)
    # feedback = filters.filter(Feedback.objects.all().select_related('platform')).order_by(*sorting_fields)
    feedback = filters.filter(Feedback.objects.all().select_related('platform')).order_by(*sorting_fields)
    return feedback


@router.post('', summary='Добавление отзыва о работе сайта', response={201: CustomerResponseOut2xx, 400: None})
def add_feedback(request: HttpRequest, data: FeedbackIn) -> Union[tuple[int, Dict[str, Any]], tuple[int, None]]:
    '''
    Метод добавления отзыва о работе сайта.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Тело запроса:
        data (FavoriteIn): данные об избранном из запроса.

    Возвращаемый результат:
        (FavoriteOut): json данных об избранном.

    Примеры:
        >>>> add_feedback(HttpRequest(), data)
        data: {
          "customer_id": 147224,
          "item_id": 10
        }
        response: {
          "id": 10,
          "customer_id": 14722,
          "item_id": 120,
          "created_at": "2024-01-09T08:38:32.923Z"
        }
    '''
    data_dict = data.dict()
    # Создаем объект feedback
    feedback = Feedback()

    # Устанавливаем автора обратной связи и платформу
    feedback.customer = get_customer_deleted_none(data_dict.pop('customer_id', None), return_error=False, only_fields=['id'])
    feedback.platform = get_or_create_platform(data_dict.pop('platform', None))

    for attr, value in data_dict.items():
        if value:
            setattr(feedback, attr, value)

    feedback.save()

    answer = {'data': [{'id': feedback.id}]}

    return 201, answer


@router.get('{feedback_id}/', summary='Просмотр отзыва', response=FeedbackOut)
def get_feedback(request: HttpRequest, feedback_id: int) -> Feedback:
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
    feedback = get_object_or_404(Feedback.objects.select_related('platform'), id=feedback_id)

    return feedback


@router.delete(
    '{feedback_id}/',
    summary='Удаление отзыва о работе сайта',
    response={200: None, 400: None}
)
def delete_feedback(request: HttpRequest, feedback_id: int) -> tuple[int, None]:
    '''
    Метод удаления отзыва о работе сайта.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Тело запроса:
        data (FavoriteDelete): данные об избранном из запроса (id избранных для удаления).

    Возвращаемый результат:
        (CustomerResponseOut): json ответа выполнения операции.

    Примеры:
        >>>> delete_feedback(HttpRequest(), {"id": [1, 2, 3]})
        response: {
          "success": true,
          "message": null,
          "data": {
            "count_deleted": 2
          }
        }
    '''
    number = Feedback.objects.filter(id=feedback_id).delete()
    if number:
        # Запись была удалена
        return 200, None
    return 400, None
