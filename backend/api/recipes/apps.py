''' Configuration for 'recipes' API application. '''

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    '''
    Encapsulate config options for 'recipes' API application.
    '''
    name = label = 'api.recipes'
