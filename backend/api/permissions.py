''' Permissions classes for API. '''

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrAdminOrReadOnly(BasePermission):
    ''' Allows access only to admin or object author user. '''

    message = _('You can change only own content!')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff)
