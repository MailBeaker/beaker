
from django.conf.urls import patterns, url, include


from rest_framework.routers import SimpleRouter


from api_service import views as service_views


router = SimpleRouter()
router.register('users', service_views.UserViewSet)
router.register('user-metas', service_views.UserMetaViewSet)
router.register('organizations', service_views.OrganizationViewSet)
router.register('domains', service_views.DomainViewSet)
router.register('links', service_views.LinkViewSet)
router.register('attachments', service_views.AttachmentViewSet)
router.register('rules', service_views.RuleViewSet)
router.register('messages', service_views.MessageViewSet)
router.register('emails', service_views.EmailMetaViewSet)


urlpatterns = patterns(
    '',
    url(r'organizations/(?P<pk>[a-z0-9]+)/users$', service_views.OrganizationUsersView.as_view(), name='service-organization-user-list'),
    url(r'domains/(?P<pk>[a-z0-9]+)/users$', service_views.DomainUsersView.as_view(), name='service-domain-user-list'),
    url(r'rules/(?P<pk>[a-z0-9]+)/matches$', service_views.RuleMatchView.as_view(), name='service-rules-matches-list'),
    url(r'^$', service_views.ServiceAPIRootView.as_view(), name='service-api-root'),
    url(r'', include(router.urls)),
)
