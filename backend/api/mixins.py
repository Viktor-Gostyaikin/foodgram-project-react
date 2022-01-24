''' Mixins classes for API. '''

from rest_framework import serializers


class SerializerMethodFieldMixin(serializers.Serializer):

    def get_exists(self, related_manager, **kwargs):
        user = self.context['request'].user
        return (False if user.is_anonymous else getattr(
            user, related_manager
        ).filter(**kwargs).exists())
