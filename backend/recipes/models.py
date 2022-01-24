from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Tag(models.Model):
    ''' Stores a single tag entry. '''
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        null=False,
    )
    color = models.CharField(
        verbose_name=_('Color') + 'HEX',
        help_text=_('''The tag's color'''),
        max_length=7,
        null=True,
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=150,
        help_text=_('''The tag's slug'''),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        ''' Return tag name. '''
        return self.name


class Ingredient(models.Model):
    ''' Stores a single ingredient entry. '''
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        unique=True,
        help_text=_('''The ingredient's name'''),
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=200,
        help_text=_('''The ingredient's measurement unit'''),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        ''' Return ingredient name. '''
        return self.name


class Recipe(models.Model):
    '''
    Stores a single recipe entry, related to
    :model:'users.User' as author.
    '''
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        help_text=_('''The recipe's name'''),
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('Author'),
        help_text=_('''The recipe's author'''),
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name=_('Image'),
        help_text=_('''The recipe's image'''),
    )
    text = models.TextField(
        verbose_name=_('Description'),
        help_text=_('''The recipe's description'''),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Cooking time'),
        help_text=_('''The recipe's cooking time'''),
        validators=[MinValueValidator(
            1, message='The time value must be >=1')],
    )
    created = models.DateTimeField(
        verbose_name=_('Publication date'),
        help_text=_('''The recipe's publication date'''),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        ''' Return recipe name. '''
        return self.name


class RecipeTag(models.Model):
    '''
    Stores the m2m relation between :model:'foodgram.Recipe'
    and :model:'foodgram.Tag'.
    '''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name=_('Recipe')
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Tag')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag_exists'
            ),
        ]
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        ''' Return tag's name. '''
        return self.tag.name


class RecipeIngredient(models.Model):
    '''
    Stores the m2m relation between :model:'foodgram.Recipe'
    and :model:'foodgram.Ingredient'.
    '''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name=_('Recipe'),
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Ingredient'),
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('Amount'),
        help_text=_('''The ingredient amount'''),
        validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_exists'
            ),
        ]
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        ''' Return ingredient's name. '''
        return self.ingredient.name


class FavoriteRecipe(models.Model):
    '''
    Stores the m2m relation between :model:'foodgram.Recipe'
    and :model:'users.User'.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name=_('User')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Recipe')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='favorite_recipe_user_exists'
            ),
        ]
        verbose_name = _('Favorite recipe')
        verbose_name_plural = _('Favorite recipes')


class RecipeShoppingCart(models.Model):
    '''
    Stores the m2m relation between :model:'foodgram.Recipe'
    and :model:'users.User'.
    '''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Recipe')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name=_('User')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='shopping_recipe_user_exists'
            ),
        ]
        verbose_name = verbose_name_plural = _('Shopping cart')
