'''Модуль для описания схем представления данных обратной связи от пользователей сайта.'''
from datetime import date
from typing import Any, List, Optional, Union

from ninja.pagination import paginate, PaginationBase
from ninja_extra.ordering import OrderingBase, ordering
from ninja import Field, FilterSchema, ModelSchema, Schema
from pydantic import HttpUrl, root_validator
from django.db.models import QuerySet

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


class OutputMeta(Schema):
    total: int = None
    per_page: int = None


class PaginationFilter(PaginationBase):
    class Input(Schema):
        page: int = Field(None, alias='pagination[page]')
        page_size: int = Field(None, alias='pagination[page_size]')
        with_count: bool = Field(True, alias='pagination[with_count]')

    class Output(Schema):
        data: List[Any]
        meta: OutputMeta

    items_attribute: str = 'data'

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        page_size = pagination.page_size
        with_count = pagination.with_count

        queryset_result = queryset

        meta = {}

        if page is not None and page_size is not None:
            # Так как page начинается с 1, то при срезе уменьшаем его на 1
            page_limit = (page-1)*page_size
            queryset_result = queryset_result[page_limit:page_limit + page_size]
            meta['per_page'] = page

        if with_count:
            meta['total'] = queryset_result.count()

        return {
            'data': queryset_result,
            'meta': meta
        }


def check_sum(values):
    sort, sort_0, sort_1 = values.get('sort'), values.get('sort_0'), values.get('sort_1')
    values['ordering'] = [sort, sort_0, sort_1]
    return values


# class OrderingFilter(OrderingBase):
#     pass
    # class Input(Schema):
    #     sort: Optional[str] = Field(None, alias='sort')
    #     sort_0: Optional[str] = Field(None, alias='sort[0]')
    #     sort_1: Optional[str] = Field(None, alias='sort[1]')
    #     ordering = None
    #
    #     # root_validator('*', allow_reuse=True)(check_sum)
    #
    # def __init__(
    #     self,
    #     ordering_fields: Optional[List[str]] = None,
    #     pass_parameter: Optional[str] = None,
    # ) -> None:
    #     super().__init__(pass_parameter=pass_parameter)
    #     self.ordering_fields = ordering_fields or "__all__"
    #
    # def ordering_queryset(
    #     self, items: Union[QuerySet, List], ordering_input: Input
    # ) -> Union[QuerySet, List]:
    #
    #     raw_fields_sorting = [ordering_input.sort, ordering_input.sort_0, ordering_input.sort_1]
    #     fields_sorting = self.get_ordering(items, raw_fields_sorting)
    #     if fields_sorting:
    #         if isinstance(items, QuerySet):  # type:ignore
    #             return items.order_by(*fields_sorting)
    #     return items
    #
    # def get_ordering(
    #     self, items: Union[QuerySet, List], fields: Optional[List[str]]
    # ) -> List[str]:
    #     if fields:
    #         new_fields = []
    #         # Обработка строки сортировки
    #         # Возможные варианты: sort=rating, sort=id:asc, sort[0]=url:asc, sort[1]=rating:desc
    #         for field in fields:
    #             list_field = field.split(':')
    #             if len(list_field) == 2:
    #                 if list_field[1] == 'desc':
    #                     list_field[0] = '-' + list_field[0]
    #             new_fields.append(list_field[0])
    #             print(new_fields)
    #
    #         return self.remove_invalid_fields(items, new_fields)
    #     return []
    #
    # def remove_invalid_fields(
    #     self, items: Union[QuerySet, List], fields: List[str]
    # ) -> List[str]:
    #     valid_fields = list(self.get_valid_fields(items))
    #
    #     def term_valid(term: str) -> bool:
    #         if term.startswith("-"):
    #             term = term[1:]
    #         return term in valid_fields
    #
    #     return [term for term in fields if term_valid(term)]
    #
    # def get_valid_fields(self, items: Union[QuerySet, List]) -> List[str]:
    #     valid_fields: List[str] = []
    #     if self.ordering_fields == "__all__":
    #         if isinstance(items, QuerySet):  # type:ignore
    #             valid_fields = self.get_all_valid_fields_from_queryset(items)
    #     else:
    #         valid_fields = list(self.ordering_fields)
    #     return valid_fields
    #
    def get_all_valid_fields_from_queryset(self, items: QuerySet) -> List[str]:
        items.model._meta.fields
        return [str(field.name) for field in items.model._meta.fields] + [
            str(key) for key in items.query.annotations
        ]



class FeedbackFilter(FilterSchema):
    '''Схема FILTER для обратной связи.'''

    id: Optional[int] = None
    comment: str = Field(None, q='comment__icontains')
    rating__in: List[int] = Field(None, ge=1, le=5, alias='rating')
    created_at: Optional[date] = None
    customer_id__in: List[int] = Field(None, alias='customer_id')
    platform_id__in: List[int] = Field(None, alias='platform_id')

    sort: Optional[str] = Field(None, alias='sort')
    sort_0: Optional[str] = Field(None, alias='sort[0]')
    sort_1: Optional[str] = Field(None, alias='sort[1]')


class FeedbackDelete(FilterSchema):
    '''Схема DELETE для обратной связи.'''

    id: int = Field(None, alias='id')
