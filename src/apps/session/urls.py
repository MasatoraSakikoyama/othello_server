# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.session.apis import Account, Authenticate, Unauthenticate

urlpatterns = [
    url(r'^account', Account.as_view(), name='account'),
    url(r'^authenticate', Authenticate.as_view(), name='authenticate'),
    url(r'^unauthenticate', Unauthenticate.as_view(), name='unauthenticate'),
]
