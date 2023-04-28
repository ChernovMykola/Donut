from django.core.management.base import BaseCommand
from donut_app.models import Donut
from faker import Faker
import random
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Generates 200 fake Donut objects'

    def handle(self, *args, **options):
        faker = Faker()
        pictures_dir = os.path.join(settings.MEDIA_DIR, 'donut_pictures')
        picture_files = os.listdir(pictures_dir)
        picture_files = random.sample(picture_files, 20)
        donut_names = [
            'Glazed',
            'Chocolate Sprinkles',
            'Maple Bacon',
            'Blueberry Cake',
            'Cinnamon Sugar',
            'Raspberry Jelly',
            'Apple Fritter',
            'Boston Cream',
            'Lemon Zest',
            'Pistachio Honey',
            'Strawberry Shortcake',
            "S'mores",
            'Red Velvet',
            'Chocolate Chip',
            'Pumpkin Spice',
            'Salted Caramel',
            'Oreo',
            'Matcha Green Tea',
            'Tiramisu',
            'Vanilla Bean',
        ]

        # Define a list of donut labels
        donut_labels = ['GF', 'VE']

        # Define a list of ingredients
        ingredients = ['flour', 'sugar', 'butter', 'milk', 'eggs']

        # Define a list of allergens
        allergens = ['nuts', 'soy', 'milk', 'wheat', 'eggs']

        # Define a list of prices
        prices = [1.99, 2.99, 0.99, 1.59, 2.59]
        # Use the Donut model to create 200 objects

        for i in range(200):
            donut = Donut(
                name=random.choice(donut_names),
                picture=random.choice(picture_files),
                title=faker.sentence(),
                description=faker.paragraph(),
                stars=faker.random_int(min=1, max=5),
                labels=random.choice(donut_labels),
                ingredients=random.choice(ingredients),
                allergens=random.choice(allergens),
                price=random.choice(prices),
                count=faker.random_int(min=0, max=100)
            )
            donut.save()
