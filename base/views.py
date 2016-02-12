
import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.html import mark_safe
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from authentication import models as auth_models
from authentication import serializers as auth_serializers

from beaker import serializers as beaker_serializers


def webapp_meta(request):
    user = request.user

    meta = {
        'user': None,
        'organization': None,
    }

    if user and user.is_authenticated():
        user_meta = auth_models.UserMeta.get_by_user(user)
        organization = user_meta.organization if user_meta else None

        meta = {
            'user': auth_serializers.UserSerializer(user, context={'request': request}, read_only=True).data,
            'organization': beaker_serializers.OrganizationSerializer(organization, context={'request': request}, read_only=True).data,
        }

    return meta


def redirect_to_index(request):
    return redirect('/app/')


class IndexView(View):

    template_name = 'webapp.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        meta = webapp_meta(request)
        context = {'meta': mark_safe(json.dumps(meta))}

        return render(request, self.template_name, context)


class APIRootView(APIView):
    def get(self, request):
        data = [
            'Service API: %s' % reverse('service-api-root', request=request),
            'Client API: %s' % reverse('client-api-root', request=request),
            {'Other Endpoints': {
                'Webapp Meta': reverse('webapp-meta', request=request),
            }}
        ]
        return Response(data)


def webapp_meta_view(request):
    if not request.user.is_authenticated():
        data = mark_safe(json.dumps({'meta': None}))
        return HttpResponse(data, status=401, content_type="application/json")
    meta = webapp_meta(request)
    return HttpResponse(mark_safe(json.dumps(meta)), content_type="application/json")


def page_not_found(request):
    """
    If this request was for the API, raise a 404 error.  Otherwise render the angular app.
    """
    if request.path.startswith('/api/'):
        raise Http404
    return IndexView.as_view()(request)
