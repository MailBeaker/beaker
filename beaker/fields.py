
from rest_framework import serializers


class RuleRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return value.rule.id
