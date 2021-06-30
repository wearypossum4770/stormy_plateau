from os import environ
from django.core.wsgi import get_wsgi_application
environ.setdefault('DJANGO_SETTINGS_MODULE', 'stormy_plateau.settings')
application = get_wsgi_application()
