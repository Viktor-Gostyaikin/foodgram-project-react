''' Filter classes for 'recipes' API application. '''

from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, User
from rest_framework.filters import SearchFilter


class RecipeFilter(FilterSet):
    ''' Filter class for :model:'recipes.Recipe'. '''
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__tag__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def _filter_related(self, queryset, value, related_manager):
        if value and not self.request.user.is_anonymous:
            recipe_ids = related_manager.values_list(
                'recipe', flat=True
            )
            return queryset.filter(id__in=recipe_ids)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        return self._filter_related(
            queryset, value, self.request.user.favorite_recipes
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self._filter_related(
            queryset, value, self.request.user.shopping_cart
        )


class IngredientFilter(SearchFilter):
    search_param = 'name'
