'''WSGI конфигурация для vaptekecustomers.'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaptekecustomers.settings')

application = get_wsgi_application()
