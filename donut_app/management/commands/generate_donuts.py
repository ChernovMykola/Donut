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
        pictures_dir = os.path.join(settings.MEDIA_DIR)
        picture_files = os.listdir(pictures_dir)
        picture_files = random.sample(picture_files, 19)
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

        donut_description = [
            "Classic glazed with a soft, fluffy texture",
            "Chocolate lover's dream with a rich cocoa glaze",
            "Blueberry cake with a tangy fruit filling",
            "Maple bacon with savory bits of crispy bacon",
            "Cinnamon sugar with a sweet and spicy crunch",
            "Raspberry jelly with a gooey, fruity center",
            "Apple fritter with chunks of juicy apple",
            "Boston cream with creamy vanilla filling",
            "Lemon zest with a zingy citrus flavor",
            "Pistachio honey with a nutty and sweet taste",
            "Strawberry shortcake with layers of fluffy cake",
            "S'mores with gooey marshmallow and chocolate",
            "Red velvet with a moist, velvety texture",
            "Cookie dough with chunks of chocolate chip cookie",
            "Pumpkin spice with warm autumn spices",
            "Salted caramel with a sweet and salty kick",
            "Oreo with crumbled cookies and creamy filling",
            "Matcha green tea with a subtle earthy taste",
            "Tiramisu with layers of espresso-soaked ladyfingers",
            "Vanilla bean with a rich, creamy flavor"
        ]

        # Define a list of donut labels
        donut_labels = ['GF', 'VE', 'BS']

        # Define a list of ingredients
        ingredients = ['flour', 'sugar', 'butter', 'milk', 'eggs']

        # Define a list of allergens
        allergens = ['nuts', 'soy', 'milk', 'wheat', 'eggs']

        # Define a list of prices
        prices = [1.99, 2.99, 0.99, 1.59, 2.59]
        # Use the Donut model to create 200 objects

        for i in range(200):
            name = random.choice(donut_names)
            if len(name) > 100:
                name = name[:99]
            donut = Donut(
                name=name,
                title=name,
                picture=random.choice(picture_files),
                description=random.choice(donut_description),
                stars=faker.random_int(min=1, max=5),
                labels=random.choice(donut_labels),
                ingredients=random.choice(ingredients),
                allergens=random.choice(allergens),
                price=random.choice(prices),
                count=faker.random_int(min=0, max=100)
            )
            donut.save()

