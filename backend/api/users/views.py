''' Views for 'users' API application. '''

from api.recipes.serializers import UserSubscriptionSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status, validators, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SubscriptionsViewSet(viewsets.GenericViewSet):
    ''' ViewSet for user subscription actions. '''
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    @action(detail=False, methods=['get'], name='subscriptions')
    def subscriptions(self, request, pk=None):
        ''' Get list of user subscriptions. '''
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], name='subscribe')
    def subscribe(self, request, pk=None):
        ''' Process user subscription actions.. '''
        subscribed = get_object_or_404(get_user_model(), id=pk)
        if self.request.method == 'DELETE':
            request.user.subscriptions.remove(subscribed)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.user.subscriptions.filter(id=subscribed.id).exists():
            raise validators.ValidationError(
                _('The subscription already exists.')
            )
        request.user.subscriptions.add(subscribed)
        serializer = self.get_serializer(instance=subscribed)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
