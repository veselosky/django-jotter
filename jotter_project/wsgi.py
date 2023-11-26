"""
It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

PROJECT = __name__.split(".")[0]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT}.settings")

application = get_wsgi_application()
