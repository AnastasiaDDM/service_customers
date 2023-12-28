# vAptekeCustomers

Сервис для обработки данных о клиентах.

Для запуска необходимо указать следующие переменные окружения:
```
SECRET_KEY=some_string - секретный ключ
POSTGRES_DB=vaptekecustomers - название БД postgres в контейнере
POSTGRES_USER=vaptekecustomers_user - пользователь для БД postgres в контейнере
POSTGRES_PASSWORD=vaptekecustomers_password - пароль для БД postgres в контейнере
POSTGRES_HOST=vAptekeCustomers-postgresql - название контейнера БД postgres
POSTGRES_PORT=5432 - порт БД postgres

VAPTEKESYNC_DB=vAptekeSync - название БД vAptekeSync
VAPTEKESYNC_USER=vaptekesync_user - пользователь для БД vAptekeSync
VAPTEKESYNC_PASSWORD=vaptekesync_password - пароль для БД vAptekeSync
VAPTEKESYNC_HOST=192.168.123.205 - хост БД vAptekeSync
VAPTEKESYNC_PORT=1433 - порт БД vAptekeSync

MSSQL_TIMEOUT=30 - таймаут запросов к БД vAptekeSync в секундах
MSSQL_RETRIES_COUNT=2 - кол-во повторных попыток 
MSSQL_RETRIES_SLEEP=30 - пауза между попытками в секундах
```

## Доступные API-методы:

### Служебные

#### GET `/grpc/v1/service/import_customers/`

Метод для загрузки данных о зарегистрированных клиентах из БД vAptekeSync.
Сохраняет данные в таблицы БД Postgres: Phones, Firstnames, Customers.

##### Параметры
Не принимает параметры.

___

### Клиенты

#### GET `/rest/v1/customers/`

Метод получения списка неудаленных клиентов.

##### Параметры
* `limit (int)`: количество элементов в одном ответе.
* `offset (int)`: смещение (страница).

##### Ответ
`({list[dict]})`: список json данных о клиентах.

```
{
  "items": [
    {
      "id": 14722,
      "phone": {
        "id": 1,
        "code": "7",
        "number": "9025163111"
      },
      "firstname": "Виктор",
      "lastname": null,
      "email": "ving@mail.ru",
      "birthday": null
    },
    ...
      ],
  "count": 78553
}
```


#### POST `/rest/v1/customers/`

Метод создания клиента.

##### Тело запроса
* `data (dict)`: данные о клиенте из запроса.

```
{
    "phone": "50110556645",
    "firstname": "string",
    "lastname": "string",
    "email": "user@example.com",
    "birthday": "2023-12-21",
    "gender": "M",
    "city_id": 0,
    "last_auth_at": "2023-12-21T04:20:37.024Z"
}
```

##### Ответ
`(dict)`: json данных клиента.
```
{
    "id": 1,
    "phone": "50110556645",
    "firstname": "string",
    ...
}
```


#### GET `/rest/v1/customers/{customer_id}/`

Метод получения данных одного клиента (неудаленного).

##### Параметры
* `customer_id (int)`: id клиента.

##### Ответ
`(dict)`: json данных клиента.
```
{
    "id": 1,
    "phone": "50110556645",
    "firstname": "string",
    ...
}
```


#### DELETE `/rest/v1/customers/{customer_id}/`

Метод мягкого удаления клиента.

##### Параметры
* `customer_id (int)`: id клиента.

##### Ответ
`(dict)`: json ответа выполнения операции.
```
{
  "success": true,
  "message": "string"
}
```


#### PATCH `/rest/v1/customers/{customer_id}/`

Метод изменения клиента.

##### Параметры
* `customer_id (int)`: id клиента.

##### Тело запроса
* `data (dict)`: данные о клиенте из запроса.

```
{
    "firstname": "string",
    "lastname": "string",
    "email": "user@example.com",
    "birthday": "2023-12-21",
    "gender": "M",
    "city_id": 0,
    "last_auth_at": "2023-12-21T04:30:57.957Z"
}
```

##### Ответ
`(dict)`: json данных о клиенте.
```
{
    "id": 1,
    "phone": "50110556645",
    "firstname": "string",
    ...
}
```


#### PATCH `/rest/v1/customers/{customer_id}/`

Метод изменения телефона клиента.

##### Параметры
* `customer_id (int)`: id клиента.

##### Тело запроса
* `data (dict)`: данные о клиенте из запроса (телефон).

```
{
    "phone": "65979638297"
}
```

##### Ответ
`(dict)`: json ответа выполнения операции.
```
{
  "success": true,
  "message": "string"
}
```


___


### Избранное

#### GET `/rest/v1/favorites/`

Метод получения списка избранных товаров.

##### Параметры
* `limit (int)`: количество элементов в одном ответе.
* `offset (int)`: смещение (страница).
* `id (int)`: id записи.
* `user_id (list[int])`: список id клиентов (в строке запроса записывается так:
user_id=14738&user_id=14722)
* `item_id (list[int])`: список id товаров (в строке запроса записывается так:
item_id=10&item_id=12)
* `created_at (datetime)`: дата создания (добавления в избранные).

##### Ответ
`(dict{"items": list[dict], "count": int})`: список json данных об избранных.

```
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
```


#### POST `/rest/v1/favorites/`

Метод добавления товара в избранное.

##### Тело запроса
* `data (dict)`: данные об избранном из запроса.

```
{
  "user_id": 14722,
  "item_id": 10
}
```

##### Ответ
`(dict)`: json данных об избранном.
```
{
  "id": 1,
  "user_id": 14722,
  "item_id": 10,
  "created_at": "2024-01-09T08:45:19.097Z"
}
```


#### DELETE `/rest/v1/favorites/`

Метод удаления товара из избранного.

##### Тело запроса
* `data (dict)`: данные об избранном из запроса (id избранных для удаления).

```
{
  "id": [
    1,
    2,
    3
  ]
}
```

##### Ответ
`(dict)`: json ответа выполнения операции.
```
{
  "success": true,
  "message": null,
  "data": {
    "count_deleted": 2
  }
}
```
`*` В примере количество удаленных записей (`count_deleted`) - 2, так как в базе присутствовали 
только 2 записи с найденными id.