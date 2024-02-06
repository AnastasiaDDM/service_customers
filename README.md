# vAptekeCustomers

Сервис для обработки данных о пользователях.

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

Метод для загрузки данных о зарегистрированных пользователях из БД vAptekeSync.
Сохраняет данные в таблицы БД Postgres: Firstnames, Customers.

##### Параметры
Не принимает параметры.

___

### Пользователи

#### GET `/rest/v1/customers/`

Метод получения списка пользователей.

##### Параметры
* `limit (int)`: количество элементов в одном ответе.
* `offset (int)`: смещение (страница).

##### Ответ
`({list[dict]})`: список json данных о пользователях.

```
{
  "items": [
    {
      "id": 14722,
      "phone": "79025163111",
      "firstname": "Виктор",
      "lastname": null,
      "email": "ving@mail.ru",
      "birthday": null,
      ...
    },
    ...
      ],
  "count": 78553
}
```


#### POST `/rest/v1/customers/`

Метод создания пользователя.

##### Тело запроса
* `data (dict)`: данные о пользователе из запроса.

```
{
    "phone": "79016606060",
    "firstname": "string",
    "lastname": "string",
    "email": "user@example.com",
    "birthday": "2024-01-25",
    "gender": "M",
    "city_id": 0,
    "last_auth_at": "2024-01-25T08:01:19.873Z",
    "last_auth_platform": "desktop"  
}
```

##### Ответ
`(dict)`: json данных пользователя.
```
{
    "id": 1,
    "phone": "79016606060",
    "firstname": "string",
    ...
}
```


#### GET `/rest/v1/customers/{customer_id}/`

Метод получения данных одного пользователя.

##### Параметры
* `customer_id (int)`: id пользователя.

##### Ответ
`(dict)`: json данных пользователя.
```
{
    "id": 1,
    "phone": "79016606060",
    "firstname": "string",
    ...
}
```


#### DELETE `/rest/v1/customers/{customer_id}/`

Метод удаления чувствительных данных пользователя. 
Очищаются поля email, phone, firstname_id, lastname_id.

##### Параметры
* `customer_id (int)`: id пользователя.

##### Ответ
`(dict)`: json ответа выполнения операции.
```
{
  "success": true,
  "message": "string"
}
```


#### PATCH `/rest/v1/customers/{customer_id}/`

Метод изменения пользователя.

##### Параметры
* `customer_id (int)`: id пользователя.

##### Тело запроса
* `data (dict)`: данные о пользователе из запроса.

```
{
    "firstname": "string",
    "lastname": "string",
    "email": "new@example.com",
}
```

##### Ответ
`(dict)`: json данных о пользователе.
```
{
    "id": 1,
    "phone": "79110556645",
    "firstname": "string",
    "email": "new@example.com",
    ...
}
```


#### PATCH `/rest/v1/customers/{customer_id}/`

Метод изменения телефона пользователя.

##### Параметры
* `customer_id (int)`: id пользователя.

##### Тело запроса
* `data (dict)`: данные о пользователе из запроса (телефон).

```
{
    "phone": "79041480000"
}
```

##### Ответ
`(dict)`: json ответа выполнения операции.
```
{
  "success": true,
  "message": "Номер успешно изменен"
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
* `user_id (list[int])`: список id пользователей (в строке запроса записывается так:
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