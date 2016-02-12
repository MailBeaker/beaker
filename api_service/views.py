
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets

from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api_service.permissions import ServiceMixin
from api_service.permissions import SuperadminMixin

from api_service.serializers import EmailMetaSerializer

from authentication.models import EmailMeta
from authentication.models import MBUser
from authentication.models import UserMeta

from authentication.serializers import UserSerializer
from authentication.serializers import UserMetaSerializer

from beaker.models import Domain
from beaker.models import Link
from beaker.models import Attachment
from beaker.models import Message
from beaker.models import Organization
from beaker.models import Rule
from beaker.models import RuleMatch

from beaker.serializers import DomainSerializer
from beaker.serializers import LinkSerializer
from beaker.serializers import AttachmentSerializer
from beaker.serializers import MessageSerializer
from beaker.serializers import OrganizationSerializer
from beaker.serializers import RuleSerializer
from beaker.serializers import RuleMatchSerializer


class ServiceAPIRootView(ServiceMixin, APIView):
    def get(self, request):
        data = {
            'users': reverse('mbuser-list', request=request),
            'user-metas': reverse('usermeta-list', request=request),
            'organizations': reverse('organization-list', request=request),
            'domains': reverse('domain-list', request=request),
            'links': reverse('link-list', request=request),
            'attachments': reverse('attachment-list', request=request),
            'rules': reverse('rule-list', request=request),
            'messages': reverse('message-list', request=request),
            'emails': reverse('emailmeta-list', request=request),
        }
        return Response(data)


class UserViewSet(SuperadminMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MBUser.objects.all()
    serializer_class = UserSerializer

    def post_save(self, obj, created=False):
        user_meta = UserMeta.get_by_user(obj)
        if not user_meta:
            UserMeta.create_user_meta(obj)

    @detail_route(methods=['get'])
    def meta(self, request, pk=None):
        user = MBUser.objects.get(id=pk)
        user_meta = UserMeta.get_by_user(user)
        meta = UserMetaSerializer(user_meta, context={'request': request}).data
        return Response(meta)


class UserMetaViewSet(SuperadminMixin, viewsets.ModelViewSet):
    model = UserMeta
    serializer_class = UserMetaSerializer
    queryset = UserMeta.objects.all()


class AdminUserMetaListView(SuperadminMixin, generics.ListCreateAPIView):
    model = UserMeta
    serializer_class = UserMetaSerializer


class EmailMetaViewSet(ServiceMixin, viewsets.ModelViewSet):
    model = EmailMeta
    serializer_class = EmailMetaSerializer
    queryset = EmailMeta.objects.all()
    filter_fields = ('email',)


class OrganizationViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_fields = ('domain__domain_name',)


class OrganizationUsersView(ServiceMixin, generics.ListCreateAPIView):
    """
    API endpoint for users that belong to an organization
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('pk')
        if not organization_id:
            raise Http404

        organization = Organization.get_by_id(organization_id)

        metas = UserMeta.objects.filter(organization=organization)
        return [meta.user for meta in metas]


class DomainViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows domains to be viewed or edited.
    """
    model = Domain
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
    filter_fields = ('domain_name', 'organization')


class DomainUsersView(ServiceMixin, generics.ListCreateAPIView):
    """
    API endpoint for users that belong to an organization
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        domain_id = self.kwargs.get('pk')
        if not domain_id:
            raise Http404

        domain = Domain.get_by_id(domain_id)

        metas = UserMeta.objects.filter(organization=domain.organization)
        return [meta.user for meta in metas]


class RuleViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows rules to be viewed and edited.
    """
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filter_fields = ('domain__domain_name',)


class RuleMatchViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint for interacting with RuleMatches directly.
    """
    queryset = RuleMatch.objects.all()
    serializer_class = RuleMatchSerializer
    filter_fields = ('link', 'link__id')


class RuleMatchView(ServiceMixin, generics.ListCreateAPIView):

    serializer_class = RuleMatchSerializer

    def get_queryset(self):
        rule_id = self.kwargs.get('pk')
        if not rule_id:
            raise Http404

        rule = Rule.get_by_id(rule_id)
        if not rule:
            raise Http404

        matches = RuleMatch.objects.filter(rule=rule)
        return matches


class LinkViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed and edited.
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_fields = ('domain',)

    def create(self, request, *args, **kwargs):

        many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=many)

        if serializer.is_valid():
            self.object = serializer.save()
            headers = self.get_success_headers(serializer.data)

            # TODO: This errors due to DRF not being able to handle multiple created entities
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        # TODO: This errors out due to serializer.errors being a list.
        # TODO: Might be worth a PR to DRF
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows attachments to be viewed and edited.
    """
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filter_fields = ('domain',)

    def create(self, request, *args, **kwargs):

        many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=many)

        if serializer.is_valid():
            self.object = serializer.save(*args, **kwargs)
            headers = self.get_success_headers(serializer.data)

            # TODO: This errors due to DRF not being able to handle multiple created entities
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        # TODO: This errors out due to serializer.errors being a list.
        # TODO: Might be worth a PR to DRF
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(ServiceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed and edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_fields = ('domain', 'service_message_id')

    def create(self, request, *args, **kwargs):

        domain_id = request.data.get('domain', None)
        domain_name = request.data.get('domain_name', None)

        if not (domain_id or domain_name):
            return Response(
                {"errors": "domain or domain_name required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        domain = None
        if domain_id:
            domain = Domain.objects.get(pk=domain_id)

        if not domain:
            domain = Domain.objects.get(domain_name=domain_name)

        request.data['domain'] = domain.id
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object = serializer.save(*args, **kwargs)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
