"""
WSGI config for Gosocket project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/gosocket/Documents/Gosocket/Trabajo/Django_Api/Django/Gosocket/Gosocket')
sys.path.append('C:/Users/gosocket/Documents/Gosocket/Trabajo/Django_Api/Django/Gosocket')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Gosocket.settings")

application = get_wsgi_application()