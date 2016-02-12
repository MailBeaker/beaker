
from django.conf.urls import patterns, url, include


from api_client import views as client_views


user_urls = patterns(
    '',
    url(r'^(?P<pk>[a-z0-9]+)$', client_views.UserDetailView.as_view(), name='client-user-detail'),
)

organization_urls = patterns(
    '',
    url(r'^$', client_views.OrganizationListView.as_view(), name='client-organization-list'),
    url(r'^(?P<pk>[a-z0-9]+)$', client_views.OrganizationDetailView.as_view(), name='client-organization-detail'),
    url(r'^(?P<pk>[a-z0-9]+)/domains/$', client_views.OrganizationDomainView.as_view(), name='client-organization-domains'),
)

domain_urls = patterns(
    '',
    url(r'^$', client_views.DomainListView.as_view(), name='client-domain-list'),
    url(r'^(?P<pk>[a-z0-9]+)$', client_views.DomainDetailView.as_view(), name='client-domain-detail'),
    url(r'^(?P<pk>[a-z0-9]+)/rules/$', client_views.DomainRulesView.as_view(), name='client-domain-rules-list'),
    url(r'^(?P<pk>[a-z0-9]+)/users/$', client_views.DomainUserView.as_view(), name='client-domain-users-list'),
    url(r'^(?P<pk>[a-z0-9]+)/emails/$', client_views.DomainEmailView.as_view(), name='client-domain-email-list'),
    # url(r'^(?P<domain_pk>[a-z0-9]+)/emails/(?P<email_pk>[a-z0-9]+)$', client_views.DomainEmailDetailView.as_view(), name='client-domain-email-detail'),
    url(r'^(?P<pk>[a-z0-9]+)/whitelist/$', client_views.DomainWhitelistView.as_view(), name='client-domain-whitelist-list'),
    url(r'^(?P<pk>[a-z0-9]+)/blacklist/$', client_views.DomainBlacklistView.as_view(), name='client-domain-blacklist-list'),
)

rule_urls = patterns(
    '',
    url(r'^$', client_views.RuleListView.as_view(), name='client-rule-list'),
    url(r'^(?P<pk>[a-z0-9]+)$', client_views.RuleDetailView.as_view(), name='client-rule-detail'),
)

email_urls = patterns(
    '',
    url(r'^$', client_views.EmailListView.as_view(), name='client-email-list'),
    url(r'^(?P<pk>[a-z0-9]+)$', client_views.EmailDetailView.as_view(), name='client-email-detail'),
)


urlpatterns = patterns(
    '',
    url(r'^$', client_views.ClientAPIRootView.as_view(), name='client-api-root'),
    url(r'users/', include(user_urls)),
    url(r'organizations/', include(organization_urls)),
    url(r'domains/', include(domain_urls)),
    url(r'rules/', include(rule_urls)),
    url(r'emails/', include(email_urls)),
)
