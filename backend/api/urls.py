''' URLs patterns for API. '''

from django.urls import include, path

urlpatterns = [
    path('', include('api.recipes.urls')),
    path('', include('api.users.urls')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
