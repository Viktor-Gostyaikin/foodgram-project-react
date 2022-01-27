''' Admin models for 'users' application. '''

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminForm, UserSubscriptionAdminForm
from .models import User, UserProxyForSubscription, UserSubscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''
    Encapsulate admin options and functionality
    for :model:users.User.
    '''
    list_display = search_fields = list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    fields = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    empty_value_display = _('-empty-')
    form = UserAdminForm


class UserSubscriptionInline(admin.TabularInline):
    '''
    Options for inline editing of :model:users.UserSubscription instances.
    '''
    model = UserSubscription
    fk_name = 'subscriber'


@admin.register(UserProxyForSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    '''
    Encapsulate admin options and functionality
    for user subscriptions.
    '''
    search_fields = list_filter = fields = readonly_fields = (
        'first_name',
        'last_name',
    )
    list_display = (
        'list_display_full_name',
        'list_display_subscriptions',
    )
    inlines = (
        UserSubscriptionInline,
    )
    empty_value_display = _('-empty-')
    form = UserSubscriptionAdminForm

    def get_queryset(self, request):
        return (super().get_queryset(request)
                       .annotate(count_subscribe=Count('subscriptions'))
                       .filter(count_subscribe__gt=0))

    def list_display_full_name(self, obj):
        return obj.get_full_name()
    list_display_full_name.short_description = _('User')

    def list_display_subscriptions(self, obj):
        return ', '.join(
            [user.get_full_name() for user in obj.subscriptions.all()]
        )
    list_display_subscriptions.short_description = _('Subscriptions')
