from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False


if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }


ALLOWED_HOSTS = [
    '.mvsm3depy3.eu-central-1.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1',
    '[::1]'
]

SECRET_KEY = os.environ['SECRET_KEY']


# S3 settings
AWS_STORAGE_BUCKET_NAME = 'ityper'
# User credentials from IAM
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# https://github.com/jschneier/django-storages/issues/28#issuecomment-265876674
# Tell django-storages to use signature version 4
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Tell django-storages that when coming up with the URL for an item in
# S3 storage, use this domain plus the path.
# This controls how the 'static' template tag gets expanded
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the 'static' template tag from 'static' or by anything else
# refers directly to STATIC_URL.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3 Boto 3 Storage when 'collectstatic' run.
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Override S3Boto3Storage in order to accomodate 'media' and 'static'
# directories in the same bucket
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticS3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaS3Boto3Storage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


try:
    from .local import *
except ImportError:
    pass
