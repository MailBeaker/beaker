
from rest_framework import serializers

from authentication.models import EmailMeta
from beaker.models import Domain
from beaker.models import Organization
from beaker.models import Rule


class EmailMetaSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    url = serializers.HyperlinkedIdentityField(view_name='client-email-detail')
    domain = serializers.HyperlinkedRelatedField(
        view_name='client-domain-detail',
        queryset=Domain.objects.all())

    class Meta:
        model = EmailMeta
        fields = (
            'id',
            'url',
            'domain',
            'email',
            'billed',
            'thumbnail_url',
            'display_name',
            'history_id',
            'whitelisted',
            'blacklisted',
        )


class RuleSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    url = serializers.HyperlinkedIdentityField(view_name='client-rule-detail')

    class Meta:
        model = Rule
        fields = (
            'id',
            'url',
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
                                                view_name='client-rule-detail')
    url = serializers.HyperlinkedIdentityField(view_name='client-domain-detail')
    organization = serializers.HyperlinkedRelatedField(
        view_name='client-organization-detail',
        queryset=Organization.objects.all())

    class Meta:
        model = Domain
        fields = (
            'id',
            'url',
            'domain_name',
            'organization',
            'rules',
            'whitelisted',
        )


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    url = serializers.HyperlinkedIdentityField(view_name='client-organization-detail')

    domains = serializers.HyperlinkedRelatedField(source='domain_set', many=True, read_only=True,
                                                  view_name='client-domain-detail')

    address_2 = serializers.CharField(required=False)

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
            'domains',
        )
