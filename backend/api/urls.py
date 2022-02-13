''' URLs patterns for API. '''

from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('api.recipes.urls')),
    path('', include('api.users.urls')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='docs'
    ),
]
