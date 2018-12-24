# -*- coding: utf-8 -*-
import uuid

from apps.session.utils import SESSION_KEY, set_session


def session_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated:
            return response
        elif request.COOKIES.get(SESSION_KEY):
            set_session(response, request.COOKIES.get(SESSION_KEY))
            return response
        else:
            set_session(response, uuid.uuid4())
            return response
    return middleware
