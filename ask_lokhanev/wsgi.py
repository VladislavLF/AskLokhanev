import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_lokhanev.settings')

application = get_wsgi_application()
