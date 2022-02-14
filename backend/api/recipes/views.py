''' Views for 'recipes' API application. '''

from api.permissions import AuthorOrAdminOrReadOnly
from api.utils import get_shopping_cart_file
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, permissions, status, validators, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    IngredientSerializer, RecipeSerializer, RecipeShortSerializer,
    TagSerializer,
)


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    ''' ViewSet for tag actions. '''
    http_method_names = ['get']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    ''' ViewSet for ingredient actions. '''
    http_method_names = ['get']
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    ''' ViewSet for recipe actions. '''
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def _set_recipe_to_related(self, related_manager):
        ''' Process common recipe actions. '''
        recipe = self.get_object()
        if self.request.method == 'DELETE':
            related_manager.get(recipe_id=recipe.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if related_manager.filter(recipe=recipe).exists():
            raise validators.ValidationError(
                _('The recipe already exists.')
            )
        related_manager.create(recipe=recipe)
        serializer = RecipeShortSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,),
            name='favorite')
    def favorite(self, request, pk=None):
        ''' Process user favorite recipe actions. '''
        return self._set_recipe_to_related(
            request.user.favorite_recipes
        )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,),
            name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        ''' Process user shopping cart actions. '''
        return self._set_recipe_to_related(
            request.user.shopping_cart
        )

    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated,),
            name='download_shopping_cart')
    def download_shopping_cart(self, request, pk=None):
        ''' Get a file with a list of ingredients from shopping cart. '''
        return get_shopping_cart_file(request.user)
