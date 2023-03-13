"""
WSGI config for myshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

application = get_wsgi_application()


# # +++++++++++ DJANGO +++++++++++
# # To use your own Django app use code like this:
# import os
# import sys

# # assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
# path = '/home/tish/E-commerce-Website/myshop'
# if path not in sys.path:
#     sys.path.insert(0, path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'myshop.settings'

