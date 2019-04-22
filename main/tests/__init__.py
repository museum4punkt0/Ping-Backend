import os
import django
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mein_objekt.settings")
django.setup()