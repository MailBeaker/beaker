
from rest_framework import serializers

from authentication.models import MBUser
from authentication.models import UserMeta


class UserMetaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserMeta
        fields = ('user', 'organization', 'url')
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(label='id')
    usermeta = UserMetaSerializer(read_only=True)

    class Meta:
        model = MBUser
        fields = ('id', 'url', 'password', 'email', 'is_admin', 'is_platform', 'is_webapp', 'usermeta')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        instance.set_password(validated_data['password'])
        instance = super(UserSerializer, self).update(instance, validated_data)
        return instance

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
