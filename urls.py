
from django.conf.urls import patterns, url, include

from base import views as base_views


handler404 = 'base.views.page_not_found'


urlpatterns = patterns(
    '',
    url(r'^api/v1/$', base_views.APIRootView.as_view(), name='api-root'),
    url(r'^api/v1/service/', include('api_service.urls')),
    url(r'^api/v1/client/', include('api_client.urls')),

    # MailBeaker authentication urls
    url(r'^api/v1/auth/login/', 'authentication.views.login_user'),
    url(r'^api/v1/auth/logout/', 'authentication.views.logout_user'),

    # Endpoint for getting webapp metadata
    url(r'^api/v1/client/meta/', 'base.views.webapp_meta_view', name='webapp-meta'),

    # Index page that serves the webapp
    url(r'^$', 'base.views.redirect_to_index', name='index'),
    url(r'^app/.*$', base_views.IndexView.as_view(), name='index-catchall'),

    # social-oauth urls for the Google login
    url('', include('social.apps.django_app.urls', namespace='social'))
)
