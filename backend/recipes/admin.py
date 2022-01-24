''' Admin models for 'recipes' application. '''

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class RecipeTagsInline(admin.TabularInline):
    '''
    Options for inline editing of :model:foodgram.Tag instances.
    '''
    model = RecipeTag
    extra = 1


class RecipeIngredientsInline(admin.TabularInline):
    '''
    Options for inline editing of :model:foodgram.Ingredient instances.
    '''
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    '''
    Encapsulate admin options and functionality
    for :model:foodgram.Recipe.
    '''
    list_display = search_fields = list_filter = (
        'name',
        'author',
    )
    fields = (
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
    )
    inlines = (
        RecipeIngredientsInline,
        RecipeTagsInline,
    )
    empty_value_display = _('-empty-')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    '''
    Encapsulate admin options and functionality
    for :model:foodgram.Ingredient.
    '''
    list_display = search_fields = list_filter = (
        'name',
        'measurement_unit',
    )
    empty_value_display = _('-empty-')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''
    Encapsulate admin options and functionality
    for :model:foodgram.Tag.
    '''
    search_fields = list_filter = (
        'name',
        'slug',
    )
    list_display = (
        'name',
        'list_display_color',
        'slug',
    )
    empty_value_display = _('-empty-')

    def list_display_color(self, obj):
        return format_html(
            '''<div style='background-color:{};height:1em;width:5em;'>
               </div>''',
            obj.color,
        )
    list_display_color.short_description = _('Color')
