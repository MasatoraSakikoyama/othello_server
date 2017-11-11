# -*- coding: utf-8 -*-
import socket

from .base import *

SECRET_KEY = '$jv3==l0@dtkongpg2np9$8x^v4g!a1lq7l5r_=y*a9@v!uos('

DEBUG = True

ALLOWED_HOSTS = ['*', 'reversi_server']

CACHES['default']['LOCATION'] = 'redis://{}:6379'.format(socket.gethostbyname('redis'))

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
