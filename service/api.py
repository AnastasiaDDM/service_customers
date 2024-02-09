'''Модуль для методов API по работе с сущностью Клиента.'''
import re

from customers.models import Customers, Firstnames
from django.db import connections
from django.http import HttpRequest, HttpResponse
#import logs
from ninja import Router
from vaptekecustomers import common

router = Router()


@router.get('import_customers/', summary='Запуск импорта зарегистрированных пользователей')
def import_customers(request: HttpRequest) -> HttpResponse:
    '''
    Метод импорта данных зарегистрированных пользователей из MSSQL vAptekeSync.

    Аргументы:
        request (HttpRequest): информация о запросе.

    Возвращаемый результат:
        (HttpResponse): возвращает строку ответа по результату импорта.

    Примеры:
        >>>> import_customers(HttpRequest())
        ('Импорт выполнен')
    '''
    #logs.info('Customers import starting.')

    customers = []
    pattern_email = r'^.{1,100}@[a-z]{2,6}\.[a-z]{2,4}$'

    try:
        # Запрос к vAptekeSync
        with connections['vAptekeSync'].cursor() as cursor:
            cursor.execute("""
                SELECT
                    ID,
                    right(phone_main, 10) as phone_main,
                    FirstFIO,
                    email_main,
                    created_at,
                    DATEADD(s, created_at, '1970-01-01') as created_at_format_datetime,
                    DATEADD(s, updated_at, '1970-01-01') as updated_at_format_datetime
                FROM ZkzClients c WITH (NOLOCK)
                WHERE c.ID IN
                    (SELECT max(a.ID)
                    FROM (SELECT
                        ID,
                        phone_main,
                        right(phone_main, 10) as phone_main_substring,
                        FirstFIO,
                        email_main,
                        max(created_at) OVER (PARTITION BY phone_main)  AS rating_in_section
                    FROM ZkzClients WITH (NOLOCK)
                    WHERE phone_main LIKE '+7__________' OR
                    phone_main LIKE '7__________' OR
                    phone_main LIKE '8__________'
                    ) a
                    JOIN ZkzClients b WITH (NOLOCK)
                    ON a.ID = b.ID
                    GROUP BY a.phone_main_substring)
                ORDER BY ID
            """)
            result = common.fetch_named(cursor)

            for row in result:

                # Имя (FirstFIO добавляем в Firstnames)
                name = str(row.get('FirstFIO', ''))[:50].title()
                fio, _ = Firstnames.objects.get_or_create(name=name)

                # Почта (проверка email_main)
                email = None
                email_main = str(row.get('email_main', '')).replace(' ', '').lower()
                # Почта соответствует маске
                if re.fullmatch(pattern_email, email_main):
                    # Email корректный
                    email = email_main

                # Создание instance Customers
                customers.append(
                    Customers(
                        id=int(row['ID']),
                        phone='7' + str(row.get('phone_main')),
                        firstname=fio,
                        email=email,
                        created_at=row.get('created_at_format_datetime'),
                        updated_at=row.get('updated_at_format_datetime')
                    )
                )

            try:
                # Добавляем клиентов в бд
                Customers.objects.bulk_create(customers, ignore_conflicts=True)
            except Exception:
                #logs.exception_caught('Error adding customers to Postgres.')
                return HttpResponse(
                    'Импорт не выполнен. Ошибка добавления пользователей в Postgres.'
                )

    except Exception:
        #logs.exception_caught('Error importing from MSSQL vAptekeSync.')
        return HttpResponse(
            'Импорт не выполнен. Ошибка импорта пользователей из MSSQL vAptekeSync.'
        )

    #logs.info('Customers import completed.')
    return HttpResponse('Импорт выполнен.')
