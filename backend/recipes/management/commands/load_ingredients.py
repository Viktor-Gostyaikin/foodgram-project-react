import json
import requests

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loading data from csv via url to DB'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, link: str, *args, **options):
        response = requests.get(link).text
        reader = json.loads(response)
        for row in reader:
            Ingredient.objects.get_or_create(name=row.get(
                'name'), measurement_unit=row.get('measurement_unit'))
        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
