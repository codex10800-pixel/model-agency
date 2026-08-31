import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a default superuser for Render if it does not already exist."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("RENDER_SUPERUSER_USERNAME", "siya")
        email = os.environ.get("RENDER_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("RENDER_SUPERUSER_PASSWORD", "ChangeMe123!")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
