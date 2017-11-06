# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.apiv1.apis import Initialize, Turn

urlpatterns = [
    url(r'^initialize', Initialize.as_view(), name='initialize'),
    url(r'^turn', Turn.as_view(), name='turn'),
]
