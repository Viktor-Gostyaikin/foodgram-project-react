import csv

import requests
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loading data from csv via url to DB'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, link: str, *args, **options):
        response = requests.get(link)
        reader = csv.reader(response)
        for row in reader:
            name, unit = row
            Ingredient.objects.get_or_create(name=name, unit=unit)
        # Ingridient.objects.bulk_create(
        #     [Ingridient(
        #         **{k.lower(): v for k, v in data.items()}
        #     ) for data in reader])

        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
