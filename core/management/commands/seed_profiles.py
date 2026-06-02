from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import ModelProfile, ActorProfile
import random

FIRST = [
    'Ava','Mia','Luna','Olivia','Isla','Zara','Sofia','Chloe','Grace','Ella',
    'Liam','Noah','Ethan','Mason','Logan','Lucas','James','Oliver','Henry','Leo'
]
LAST = [
    'Smith','Johnson','Brown','Williams','Jones','Davis','Miller','Wilson','Moore','Taylor',
    'Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Garcia','Martinez','Robinson'
]
HEIGHTS = ['165 cm','168 cm','170 cm','172 cm','175 cm','178 cm','180 cm','182 cm','185 cm']
LOCATIONS = ['Gqeberha','Cape Town','Johannesburg','Durban','Port Elizabeth','East London','Bloemfontein']
BIOS = [
    'A dedicated professional with a passion for editorial and runway work.',
    'Experienced in commercial and lifestyle shoots; reliable and punctual.',
    'Emerging talent with fresh energy and a strong photographic presence.',
    'Versatile performer experienced in stage and screen productions.',
    'Natural presence in front of the camera with a striking look.'
]
CATEGORIES = ['women','men','youth']

class Command(BaseCommand):
    help = 'Seed sample ModelProfile and ActorProfile entries for local development/testing.'

    def add_arguments(self, parser):
        parser.add_argument('--models', type=int, default=30, help='Number of model profiles to create')
        parser.add_argument('--actors', type=int, default=30, help='Number of actor profiles to create')

    def handle(self, *args, **options):
        num_models = options.get('models', 30)
        num_actors = options.get('actors', 30)

        created_models = 0
        created_actors = 0

        with transaction.atomic():
            for i in range(num_models):
                name = f"{random.choice(FIRST)} {random.choice(LAST)}"
                category = random.choice(CATEGORIES)
                age = random.randint(16, 35)
                height = random.choice(HEIGHTS)
                location = random.choice(LOCATIONS)
                bio = random.choice(BIOS)
                is_featured = random.random() < 0.12

                ModelProfile.objects.create(
                    name=name,
                    category=category,
                    age=age,
                    height=height,
                    location=location,
                    bio=bio,
                    profile_image='',
                    is_featured=is_featured,
                )
                created_models += 1

            for i in range(num_actors):
                name = f"{random.choice(FIRST)} {random.choice(LAST)}"
                category = random.choice(CATEGORIES)
                age = random.randint(16, 45)
                height = random.choice(HEIGHTS)
                location = random.choice(LOCATIONS)
                bio = random.choice(BIOS)
                is_featured = random.random() < 0.08

                ActorProfile.objects.create(
                    name=name,
                    category=category,
                    age=age,
                    height=height,
                    location=location,
                    bio=bio,
                    profile_image='',
                    is_featured=is_featured,
                )
                created_actors += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_models} ModelProfile and {created_actors} ActorProfile entries.'))
