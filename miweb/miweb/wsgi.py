"""
WSGI config for miweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('/miweb')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/whatever/lib/python3.8/site-packages')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miweb.settings')

application = get_wsgi_application()
