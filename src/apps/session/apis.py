# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

from apps.session.utils import check_session


@check_session
def account(request, user_id):
    if request.method == 'POST':
        user = User.objects.create_user(
            request.POST['user_id'],
            request.POST['email'],
            request.POST['password'])
        user.save()
        return JsonResponse(status=200)

    elif request.method == 'PUT':
        user = authenticate(
            user_id=request.POST.get('user_id'),
            password=request.POST.get('password'))
        if user:
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            if username:
                user.username = username
            if new_password:
                user.set_password(new_password)
            user.save()
            return JsonResponse(statis=200)
        else:
            return JsonResponse({'message': 'Invalid param'}, status=400)
    else:
        return JsonResponse(status=405)


def auth(request):
    if request.method == 'POST':
        user = authenticate(
            user_id=request.POST.get('user_id'),
            password=request.POST.get('password'))
        if user:
            login(request, user)
            return JsonResponse(status=200)
        else:
            return JsonResponse({'message': 'Invalid param'}, status=400)
    else:
        return JsonResponse(status=405)


def unauth(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse(status=200)
    else:
        return JsonResponse(status=405)
