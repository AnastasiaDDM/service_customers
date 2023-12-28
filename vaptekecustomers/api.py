'''Модуль для группировки маршрутизаторов разных приложений.'''
from customers.api import router as customers_router
from favorites.api import router as favorites_router
import logs
from ninja import NinjaAPI
from service.api import router as service_router

api = NinjaAPI(title='vAptekeCustomers')


@api.exception_handler(Exception)
def error_handler(request, exc):
    '''Общий обработчик ошибок.'''
    logs.exception_caught('API Error')
    return api.create_response(request, {'message': 'Internal server error'}, status=500)


api.add_router('/grpc/v1/service/', service_router, tags=['Служебные'])
api.add_router('/rest/v1/customers/', customers_router, tags=['Клиенты'])
api.add_router('/rest/v1/favorites/', favorites_router, tags=['Избранные товары'])
