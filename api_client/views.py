
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api_client.permissions import SafeMethodsMixin
from api_client.permissions import WebappMixin

from api_client.serializers import DomainSerializer
from api_client.serializers import EmailMetaSerializer
from api_client.serializers import OrganizationSerializer
from api_client.serializers import RuleSerializer

from authentication.models import MBUser
from authentication.models import EmailMeta
from authentication.models import UserMeta
from authentication.serializers import UserSerializer

from beaker.models import Domain
from beaker.models import Organization
from beaker.models import Rule


class ClientAPIRootView(WebappMixin, APIView):
    """
    The base API view that links to other API views.

    URL:
        /api/v<version>/client/
    """
    def get(self, request):

        user = self.request.user
        user_meta = UserMeta.get_by_user(user)
        organization = user_meta.organization if user_meta else None

        data = {
            'current_user': reverse('client-user-detail', kwargs={'pk': user.id}, request=request),
            'domains': reverse('client-domain-list', request=request),
            'emails': reverse('client-email-list', request=request),
        }

        if organization:
            data['organization'] = reverse('client-organization-detail', kwargs={'pk': organization.id}, request=request)

        return Response(data)


class UserDetailView(WebappMixin, generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing, updating and deleting a specific user.

    URL:
        /api/v<version>/client/users/

    # TODO: This endpoint is at the wrong URL
    """
    model = MBUser
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        if not user:
            raise PermissionDenied()

        user_id = self.kwargs.get('pk')

        if not str(user.id) == str(user_id):
            raise PermissionDenied()

        return user


class DomainListView(WebappMixin, generics.ListCreateAPIView):
    """
    List the Domains the User has access to.

    URL:
        /api/v<version>/client/domains/
    """
    serializer_class = DomainSerializer

    def get_queryset(self):
        user = self.request.user

        # TODO: This needs to handle multiple UserMetas in the future
        user_meta = UserMeta.get_by_user(user)
        if user_meta:
            return Domain.objects.filter(organization=user_meta.organization)
        return []


class DomainDetailView(WebappMixin, SafeMethodsMixin, generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a domain entity.

    URL:
        /api/v<version>/client/domains/<pk>
    """
    serializer_class = DomainSerializer
    safe_get_model = Domain

    def get_object(self):
        return self.org_safe_get(self.request.user, self.kwargs.get('pk'))


class DomainWhitelistView(WebappMixin, SafeMethodsMixin, generics.ListAPIView):
    """
    List the whitelisted emails for a domain.

    URL:
        /api/v<version>/client/domains/<pk>/whitelist/
    """
    serializer_class = EmailMetaSerializer
    safe_get_model = Domain

    def get_queryset(self):
        domain = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        return domain.get_whitelist()


class DomainBlacklistView(WebappMixin, SafeMethodsMixin, generics.ListAPIView):
    """
    List the blacklisted emails for a domain.

    URL:
        /api/v<version>/client/domains/<pk>/blacklist/
    """
    serializer_class = EmailMetaSerializer
    safe_get_model = Domain

    def get_queryset(self):
        domain = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        return domain.get_blacklist()


class DomainRulesView(WebappMixin, SafeMethodsMixin, generics.ListCreateAPIView):
    """
    List the rules for a given Domain.

    URL:
        /api/v<version>/client/domains/<pk>/rules/
    """
    serializer_class = RuleSerializer
    safe_get_model = Domain

    def perform_create(self, serializer):
        """
        Adding the domain to the Rule before saving it.
        """
        instance = serializer.save(
            domain=self.org_safe_get(self.request.user, self.kwargs.get('pk')))

    def get_queryset(self):
        domain = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        return Rule.objects.filter(domain=domain)


class DomainUserView(WebappMixin, SafeMethodsMixin, generics.ListAPIView):
    """
    List the UserMetas for a given Domain.

    URL:
        /api/v<version>/client/domains/<pk>/users/
    """
    serializer_class = UserSerializer
    safe_get_model = Domain

    def get_queryset(self):
        domain = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        metas = UserMeta.objects.filter(organization=domain.organization)
        return [meta.user for meta in metas]


class DomainEmailView(WebappMixin, SafeMethodsMixin, generics.ListCreateAPIView):
    """
    List the EmailMetas for a given Domain.

    URL:
        /api/v<version>/client/domain/<pk>/emails/
    """
    serializer_class = EmailMetaSerializer
    safe_get_model = Domain

    # TODO: Add permission checks for creating a Domain

    def get_queryset(self):
        domain = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        return EmailMeta.objects.filter(domain=domain)


class EmailListView(WebappMixin, generics.ListCreateAPIView):
    """
    List all the EmailMetas that a user has access to.
    """
    serializer_class = EmailMetaSerializer

    def get_queryset(self):

        user = self.request.user
        user_meta = UserMeta.get_by_user(user)

        domains = []
        if user_meta:
            domains = Domain.objects.filter(organization=user_meta.organization)

        if not domains:
            return []

        emails = set()
        for domain in domains:
            domain_emails = EmailMeta.objects.filter(domain=domain)
            for domain_email in domain_emails:
                emails.add(domain_email)

        return list(emails)


class EmailDetailView(WebappMixin, SafeMethodsMixin, generics.RetrieveUpdateAPIView):
    serializer_class = EmailMetaSerializer
    safe_get_model = EmailMeta

    def get_object(self):
        return self.org_safe_get(self.request.user, self.kwargs.get('pk'))


class OrganizationListView(WebappMixin, generics.ListAPIView):
    """
    List all the Organizations the user has access to.

    URL:
        /api/v<version>/client/organizations/
    """
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        user_meta = UserMeta.get_by_user(user)
        return Organization.objects.filter(id=user_meta.organization.id)


class OrganizationDetailView(WebappMixin, SafeMethodsMixin, generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a given Organization.

    URL:
        /api/v<version>/client/organizations/<pk>
    """
    serializer_class = OrganizationSerializer
    safe_get_model = Organization

    def get_object(self):
        return self.org_safe_get(self.request.user, self.kwargs.get('pk'))


class OrganizationDomainView(WebappMixin, SafeMethodsMixin, generics.ListAPIView):
    """
    List all of the Domains for a given Organization.

    URL:
        /api/v<version>/client/organizations/<pk>/domains/
    """
    serializer_class = DomainSerializer
    safe_get_model = Organization

    def get_queryset(self):
        organization = self.org_safe_get(self.request.user, self.kwargs.get('pk'))
        return Domain.objects.filter(organization=organization)


class RuleListView(WebappMixin, generics.ListCreateAPIView):
    """
    List the Rules a user has access to.

    URL:
        /api/v<version>/client/rules/
    """
    serializer_class = RuleSerializer

    def get_queryset(self):

        user = self.request.user
        user_meta = UserMeta.get_by_user(user)

        domains = []
        if user_meta:
            domains = Domain.objects.filter(organization=user_meta.organization)

        if not domains:
            return []

        rules = set()
        for domain in domains:
            domain_rules = Rule.objects.filter(domain=domain)
            for domain_rule in domain_rules:
                rules.add(domain_rule)

        return list(rules)


class RuleDetailView(WebappMixin, SafeMethodsMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a given Rule.

    URL:
        /api/v<version>/client/rules/<pk>
    """
    serializer_class = RuleSerializer
    safe_get_model = Rule

    def get_object(self):
        return self.org_safe_get(self.request.user, self.kwargs.get('pk'))
