

from rest_framework import serializers

from authentication.models import EmailMeta
from beaker.models import Domain


class EmailMetaSerializer(serializers.HyperlinkedModelSerializer):

    domain_url = serializers.HyperlinkedRelatedField(source='domain', view_name='domain-detail',
                                                     queryset=Domain.objects.all())

    class Meta:
        model = EmailMeta
        fields = (
            'id',
            'url',
            'domain_url',
            'email',
            'billed',
            'whitelisted',
            'blacklisted',
            'thumbnail_url',
            'history_id',
            'display_name',
        )
