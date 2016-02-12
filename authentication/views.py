
import logging
import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.http import HttpResponse

from base import views as base_views


def login_user(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        meta_data = json.dumps(base_views.webapp_meta(request))
        return HttpResponse(content=meta_data, content_type="application/json")

    logging.warning("Username")
    return HttpResponse(status=401, content_type="application/json")


def logout_user(request):
    logout(request)
    return HttpResponse(status=200)
