# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/', include('apps.apiv1.urls'), name='apiv1'),
]
