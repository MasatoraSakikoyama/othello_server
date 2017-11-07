# -*- coding: utf-8 -*-
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = ''

DEBUG = false

ALLOWED_HOSTS = []

CACHES['default']['LOCATION'] = 'redis://127.0.0.1:6379')

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
    }
}
