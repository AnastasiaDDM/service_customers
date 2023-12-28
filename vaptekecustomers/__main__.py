'''Модуль инициализации uvicorn сервера для приложения.'''
import asyncio
import os
import sys

API_WORKERS = os.environ['API_WORKERS']


async def main():
    '''Входная функция.'''
    # Применение миграций в БД
    migrations_process = await asyncio.create_subprocess_exec(
        'python',
        'manage.py',
        'migrate'
    )

    await migrations_process.wait()

    # Запуск сервера API
    api_server = await asyncio.create_subprocess_exec(
        'python', '-m', 'gunicorn', 'vaptekecustomers.asgi:application',
        '-b', '0.0.0.0:8000', '-w', str(API_WORKERS),
        '-k', 'uvicorn.workers.UvicornWorker'
    )

    await api_server.wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException:
        sys.exit(1)
