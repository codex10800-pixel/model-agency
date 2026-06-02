import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import ModelProfile, ActorProfile


class Command(BaseCommand):
    help = 'Import profiles from a CSV file. Usage: manage.py import_profiles --type model|actor --csv path/to/file.csv'

    def add_arguments(self, parser):
        parser.add_argument('--type', choices=['model', 'actor'], required=True, help='Type of profile to import')
        parser.add_argument('--csv', required=True, help='Path to CSV file')

    def handle(self, *args, **options):
        profile_type = options['type']
        csv_path = options['csv']
        created = 0
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    name = row.get('name') or row.get('title')
                    if not name:
                        continue
                    age = row.get('age')
                    try:
                        age = int(age) if age else None
                    except ValueError:
                        age = None

                    defaults = {
                        'bio': row.get('bio', '') or '',
                        'location': row.get('location', '') or '',
                        'height': row.get('height', '') or '',
                        'is_featured': row.get('is_featured', '').lower() in ('1', 'true', 'yes'),
                        'category': row.get('category', 'women') or 'women',
                    }

                    if profile_type == 'model':
                        obj, created_flag = ModelProfile.objects.get_or_create(name=name, defaults={**defaults, 'age': age or 0})
                    else:
                        obj, created_flag = ActorProfile.objects.get_or_create(name=name, defaults={**defaults, 'age': age or 0})

                    if created_flag:
                        created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} {profile_type} profiles from {csv_path}'))
