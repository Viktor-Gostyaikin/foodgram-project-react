''' Serializers classes for 'users' API application. '''

from api import mixins
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(
        serializers.ModelSerializer,
        mixins.SerializerMethodFieldMixin):
    ''' Serializer for :model:'users.User'. '''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return self.get_exists('subscriptions', id=obj.id)
