"""
WSGI config for laboratorio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PROJECT)

os.environ['DJANGO_SETTINGS_MODULE'] = "laboratorio.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laboratorio.settings")

application = get_wsgi_application()
