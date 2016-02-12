
from beaker.fields import RuleRelatedField

from beaker.models import Domain
from beaker.models import Link
from beaker.models import Attachment
from beaker.models import Message
from beaker.models import Organization
from beaker.models import Rule
from beaker.models import RuleMatch

from rest_framework import serializers


class RuleSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')

    organization_id = serializers.ReadOnlyField(source='domain.organization.id')
    organization_url = serializers.HyperlinkedIdentityField(source='domain.organization', view_name='organization-detail')

    domain = serializers.SlugRelatedField(slug_field='id', queryset=Domain.objects.all())
    domain_id = serializers.ReadOnlyField(source='domain.id')
    domain_url = serializers.HyperlinkedIdentityField(source='domain', view_name='domain-detail')
    domain_name = serializers.ReadOnlyField(source='domain.domain_name')

    class Meta:
        model = Rule
        fields = (
            'id',
            'url',
            'domain_url',
            'organization_url',
            'domain_id',
            'domain_name',
            'organization_id',
            'domain',
            'description',
            'alert_admins',
            'action',
            'sender_mod',
            'sender_value',
            'receiver_mod',
            'receiver_value',
            'subject_mod',
            'subject_value',
            'url_mod',
            'url_value',
            'body_mod',
            'body_value',
        )


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    rules = serializers.HyperlinkedRelatedField(source='rule_set', many=True, read_only=True,
                                                view_name='rule-detail')
    organization_url = serializers.HyperlinkedIdentityField(source='domain.organization',
                                                            view_name='organization-detail')

    class Meta:
        model = Domain
        fields = (
            'id',
            'url',
            'domain_name',
            'organization_url',
            'organization',
            'rules',
            'whitelisted',
        )


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')

    domains = serializers.HyperlinkedRelatedField(source='domain_set', many=True, read_only=True,
                                                  view_name='domain-detail')

    address_2 = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Organization
        fields = (
            'id',
            'url',
            'name',
            'address_1',
            'address_2',
            'city',
            'state',
            'phone',
            'zip',
            'domains',
        )


class RuleLinkSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    rule = RuleSerializer()

    class Meta:
        model = RuleMatch
        fields = (
            'id',
            'rule',
        )


class LinkSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(read_only=True)

    domain = serializers.SlugRelatedField(slug_field='id', queryset=Domain.objects.all())
    domain_url = serializers.HyperlinkedRelatedField(source='domain', view_name='domain-detail',
                                                     read_only=True)

    message = serializers.SlugRelatedField(slug_field='id', queryset=Message.objects.all())
    message_url = serializers.HyperlinkedRelatedField(source='message', view_name='message-detail',
                                                      read_only=True)

    # matched_rules = serializers.SerializerMethodField(source='get_matched_rules', many=True, view_name='rule-detail')
    rules = RuleRelatedField(source='rulematch_set', many=True, read_only=True)

    class Meta:
        model = Link
        fields = (
            'id',
            'url',
            'redirect_url',
            'domain',
            'domain_url',
            'message',
            'message_url',
            'scheme',
            'netloc',
            'path',
            'params',
            'query',
            'fragment',
            'username',
            'password',
            'hostname',
            'port',
            'rules',
        )


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    domain = serializers.SlugRelatedField(slug_field='id', queryset=Domain.objects.all())
    domain_url = serializers.HyperlinkedRelatedField(source='domain', view_name='domain-detail',
                                                     read_only=True)

    message = serializers.SlugRelatedField(slug_field='id', queryset=Message.objects.all())
    message_url = serializers.HyperlinkedRelatedField(source='message', view_name='message-detail',
                                                      read_only=True)

    class Meta:
        model = Attachment
        fields = (
            'id',
            'url',
            'domain',
            'domain_url',
            'message',
            'message_url',
            'hash',
            'name',
            'size',
        )


class MessageSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')

    attachments = serializers.HyperlinkedRelatedField(many=True, source='attachment_set',
                                                      view_name='attachment-detail', read_only=True)
    links = serializers.HyperlinkedRelatedField(many=True, source='link_set',
                                                view_name='link-detail', read_only=True)

    domain = serializers.SlugRelatedField(
        slug_field='id', queryset=Domain.objects.all()
    )

    domain_url = serializers.HyperlinkedRelatedField(source='domain', view_name='domain-detail', read_only=True)
    message_from_address = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = (
            'id',
            'url',
            'domain',
            'domain_url',
            'links',
            'attachments',
            'message_from_address',
            'envelope_from_address',
            'rcpt_to_address',
            'service_name',
            'service_message_id',
            'authentication_results',
            'dmarc_result',
            'dkim_result',
            'spf_result',
        )


class RuleMatchSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    link = serializers.SlugRelatedField(slug_field='id', queryset=Link.objects.all())
    rule = serializers.SlugRelatedField(slug_field='id', queryset=Rule.objects.all())

    class Meta:
        model = RuleMatch
        fields = (
            'id',
            'link',
            'rule',
        )
