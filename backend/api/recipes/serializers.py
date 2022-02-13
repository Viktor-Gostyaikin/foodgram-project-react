''' Serializers for 'recipes' API application. '''
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api import fields, mixins
from api.users.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class TagSerializer(serializers.ModelSerializer):
    ''' Serializer class for :model:'recipes.Tag'. '''

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeTagSerializer(serializers.ModelSerializer):
    ''' Serializer class for :model:'recipes.RecipeTag'. '''

    id = serializers.IntegerField(source='tag.id')
    name = serializers.ReadOnlyField(source='tag.name')
    color = serializers.ReadOnlyField(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug')

    def to_internal_value(self, data):
        data = super().to_internal_value({'id': data})
        try:
            return Tag.objects.get(id=data['tag']['id'])
        except Tag.DoesNotExist:
            raise ValidationError(_('Invalid data. No such tag.'))


class IngredientSerializer(serializers.ModelSerializer):
    ''' Serializer class for :model:'recipes.Ingredient'. '''

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ''' Serializer class for :model:'recipes.RecipeIngredient'. '''

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        try:
            ingredient = Ingredient.objects.get(id=data['ingredient']['id'])
        except Ingredient.DoesNotExist:
            raise ValidationError(_('Invalid data. No such tag.'))
        return ingredient, data['amount']


class RecipeSerializer(
        serializers.ModelSerializer,
        mixins.SerializerMethodFieldMixin):
    ''' Serializer class for :model:'recipes.Recipe'. '''
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = fields.Base64ImageField(required=True)
    tags = RecipeTagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('created',)

    def validate_tags(self, value):
        if len(value) == 0:
            raise ValidationError(
                _('A recipe must have at least one tag.')
            )
        tag_ids = [tag.id for tag in value]
        unique_tag_ids = set(tag_ids)
        if len(unique_tag_ids) != len(tag_ids):
            raise ValidationError(
                _('''Invalid data. Tag's list contains duplicates.''')
            )
        return value

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise ValidationError(
                _('A recipe must have at least one ingredient.')
            )
        ingredient_ids = [ingredient.id for ingredient, _ in value]
        unique_ingredient_ids = set(ingredient_ids)
        if len(unique_ingredient_ids) != len(ingredient_ids):
            raise ValidationError(
                _('''Invalid data. Ingredient's list '''
                  '''contains duplicates.''')
            )
        return value

    def _set_tags(self, instance, tags):
        instance.tags.all().delete()
        RecipeTag.objects.bulk_create(
            [RecipeTag(recipe=instance, tag=tag) for tag in tags]
        )

    def _set_ingredients(self, instance, ingredients):
        instance.ingredients.all().delete()
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=instance,
                ingredient=ingredient,
                amount=amount) for ingredient, amount in ingredients]
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self._set_ingredients(recipe, ingredients)
        self._set_tags(recipe, tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self._set_ingredients(instance, ingredients)
        self._set_tags(instance, tags)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        return self.get_exists('favorite_recipes', recipe=obj)

    def get_is_in_shopping_cart(self, obj):
        return self.get_exists('shopping_cart', recipe=obj)


class RecipeShortSerializer(serializers.ModelSerializer):
    '''
    Serializer class with short representation
    for :model:'recipes.RecipeIngredient'.
    '''

    class Meta:
        model = Recipe
        fields = read_only_fields = (
            'id', 'name', 'image', 'cooking_time'
        )


class UserSubscriptionSerializer(UserSerializer):
    ''' Serializer class for user subscriptions. '''
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (UserSerializer.Meta.fields
                  + ('recipes', 'recipes_count',))

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        recipes_limit = (self.context['request'].query_params
                                                .get('recipes_limit'))
        if recipes_limit is not None:
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except ValueError:
                raise ValidationError(
                    _('''Parameter 'recipes_limit' excepted a int type''')
                )
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
