''' URLs patterns for 'users' API application. '''

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionsViewSet

router = DefaultRouter()
router.register('users', SubscriptionsViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]
