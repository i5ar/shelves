from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# NOTE: The request user id for debugging.
DEBUG_USER_ID = 0


# NOTE: django-rest-framework
# Override default permission for debugging purposes
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.AllowAny'
]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2@@o#qa)xros@$n)3x=(gms!5!-8ke1w$^48#w2!dsyi@eti4j'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


ALLOWED_HOSTS = ['*']


try:
    from .local import *
except ImportError:
    pass
