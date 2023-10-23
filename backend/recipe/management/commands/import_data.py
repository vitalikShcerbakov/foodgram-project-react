import csv
import os
import sys

from django.conf import settings
from django.core.management import BaseCommand

from recipe.models import Ingredient, Tag


class Command(BaseCommand):
    INITIAL_TAGS = [
        {'color': '#FF0000', 'name': 'Завтрак', 'slug': 'breakfast'},
        {'color': '#008000', 'name': 'Обед', 'slug': 'lunch'},
        {'color': '#0000FF', 'name': 'Ужин', 'slug': 'dinner'}
    ]
    DIR = '/'.join(str(settings.BASE_DIR).split('/')[:-1])
    DATA = 'data'
    FILE = 'ingredients.csv'
    help = 'Импорт данных из static/data'

    def handle(self, *args, **kwargs):
        print('Please wait...')
        try:
            with open(
                os.path.join(self.DIR, self.DATA, self.FILE),
                    mode='r', encoding='utf-8') as file:
                data = csv.reader(file, delimiter=',')
                for name, unit_type in data:
                    ingredient = Ingredient()
                    ingredient.name = name
                    ingredient.measurement_unit = unit_type
                    ingredient.save()
            for tag in self.INITIAL_TAGS:
                new_tag = Tag()
                new_tag.name = tag.get('name')
                new_tag.color = tag.get('color')
                new_tag.slug = tag.get('slug')
                new_tag.save()
            print('Data uploaded successfully')

        except FileNotFoundError:
            print(f'Файл {self.FILE} не найден.')
            sys.exit()
        except Exception as errors:
            print(errors)
