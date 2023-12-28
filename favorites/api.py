'''Модуль для методов API по работе с сущностью Клиента.'''
from typing import Dict, List

from customers.models import Customers
from customers.schemas import CustomerResponseOut
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Query, Router
from ninja.pagination import LimitOffsetPagination, paginate

from .models import Favorites
from .schemas import FavoriteDelete, FavoriteFilter, FavoriteIn, FavoriteOut


router = Router()


@router.get('', summary='Список избранных товаров', response=List[FavoriteOut])
@paginate(LimitOffsetPagination)
def list_favorites(request: HttpRequest, filters: FavoriteFilter = Query(...)) -> List[Favorites]:
    '''
    Метод получения списка избранных товаров.

    Аргументы:
        request (HttpRequest): информация о запросе.
        filters (Query): фильтры запроса из параметров.

    Параметры:
        limit (int): количество элементов в одном ответе.
        offset (int): смещение (страница).
        id (int): id записи.
        user_id (list[int]): список id клиентов (в строке запроса записывается так:
                user_id=14738&user_id=14722)
        item_id (list[int]): список id товаров (в строке запроса записывается так:
                item_id=10&item_id=12)
        created_at (datetime): дата создания (добавления в избранные).
    Возвращаемый результат:
        (dict{"items": list[dict], "count": int}): список json данных об избранных.

    Примеры:
        >>>> list_favorites(HttpRequest())
        {
          "items": [
            {
              "id": 1,
              "user_id": 14722,
              "item_id": 12,
              "created_at": null
            },
            {
              "id": 2,
              "user_id": 14738,
              "item_id": 34,
              "created_at": null
            }
          ],
          "count": 2
        }
    '''
    favorites = filters.filter(Favorites.objects.all())
    return favorites


@router.post('', summary='Добавление избранного товара', response=FavoriteOut)
def add_favorite(request: HttpRequest, data: FavoriteIn) -> FavoriteOut:
    '''
    Метод добавления избранного.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Тело запроса:
        data (FavoriteIn): данные об избранном из запроса.

    Возвращаемый результат:
        (FavoriteOut): json данных об избранном.

    Примеры:
        >>>> add_favorite(HttpRequest(), data)
        data: {
          "user_id": 147224,
          "item_id": 10
        }
        response: {
          "id": 10,
          "user_id": 14722,
          "item_id": 120,
          "created_at": "2024-01-09T08:38:32.923Z"
        }
    '''
    data_dict = data.dict()

    # Получаем клиента
    customer = get_object_or_404(Customers, pk=data_dict['user_id'])

    # Добавляем или получаем из базы избранное
    favorite, _ = Favorites.objects.get_or_create(
        user=customer,
        item_id=data_dict['item_id'],
    )
    favorite.created_at = timezone.now()
    favorite.save(update_fields=['created_at'])
    return favorite


@router.delete(
    '',
    summary='Удаление товара из избранного',
    response=CustomerResponseOut
)
def delete_favorite(
        request: HttpRequest,
        data: FavoriteDelete
) -> Dict[str, str | bool | None | Dict]:
    '''
    Метод удаления товара из избранного.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Тело запроса:
        data (FavoriteDelete): данные об избранном из запроса (id избранных для удаления).

    Возвращаемый результат:
        (CustomerResponseOut): json ответа выполнения операции.

    Примеры:
        >>>> delete_favorite(HttpRequest(), {"id": [1, 2, 3]})
        response: {
          "success": true,
          "message": null,
          "data": {
            "count_deleted": 2
          }
        }
    '''
    count_deleted, _ = data.filter(Favorites.objects.all()).delete()
    return {'success': True, 'message': None, 'data': {'count_deleted': count_deleted}}
