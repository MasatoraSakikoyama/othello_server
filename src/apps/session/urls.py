# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.session.apis import account, auth, unauth

urlpatterns = [
    url(r'^account', account, name='account'),
    url(r'^authenticate', auth, name='auth'),
    url(r'^unauthenticate', unauth, name='unauth'),
]
