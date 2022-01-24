''' Admin panel settings for project. '''

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.site_header = _('Foodgram site admin panel')
admin.site.site_title = admin.site.index_title = _('Foodgram administration')
