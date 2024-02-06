'''Модуль для группировки маршрутизаторов разных приложений.'''
from basket.api import router as basket_router
from customers.api import router as customers_router
from favorites.api import router as favorites_router
from feedback.api import router as feedback_router
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
api.add_router('/rest/v1/customers/', customers_router, tags=['Пользователи'])
api.add_router('/rest/v1/favorites/', favorites_router, tags=['Избранные товары'])
api.add_router('/rest/v1/basket/', basket_router, tags=['Корзина'])
api.add_router('/rest/v1/feedback/', feedback_router, tags=['Обратная связь'])
