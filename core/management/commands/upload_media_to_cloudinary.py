from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from django.conf import settings
import os

from core.models import ModelProfile, ActorProfile, PortfolioImage, ActorPortfolioImage


class Command(BaseCommand):
    help = 'Upload existing local MEDIA files referenced by models to the configured default storage (e.g. Cloudinary)'

    def handle(self, *args, **options):
        uploaded = 0

        def process_queryset(qs, field_name, label):
            nonlocal uploaded
            for obj in qs:
                field = getattr(obj, field_name)
                if not field:
                    continue
                # skip if already points to a remote URL
                try:
                    url = field.url
                except Exception:
                    url = None
                if url and url.startswith('http'):
                    self.stdout.write(f"{label} id={obj.id} already remote, skipping")
                    continue

                # try to locate the local file
                local_path = None
                try:
                    local_path = field.path
                except Exception:
                    # Field may store only name
                    if field.name:
                        local_path = os.path.join(settings.MEDIA_ROOT, field.name)

                if not local_path or not os.path.exists(local_path):
                    self.stdout.write(f"{label} id={obj.id} local file not found: {local_path}")
                    continue

                with open(local_path, 'rb') as fh:
                    django_file = DjangoFile(fh)
                    # re-save to trigger upload to default storage
                    field.save(os.path.basename(local_path), django_file, save=True)
                    uploaded += 1
                    self.stdout.write(f"Uploaded {label} id={obj.id} -> storage")

        # Process main profile images
        process_queryset(ModelProfile.objects.all(), 'profile_image', 'ModelProfile')
        process_queryset(ActorProfile.objects.all(), 'profile_image', 'ActorProfile')

        # Process portfolio images
        process_queryset(PortfolioImage.objects.all(), 'image', 'PortfolioImage')
        process_queryset(ActorPortfolioImage.objects.all(), 'image', 'ActorPortfolioImage')

        self.stdout.write(self.style.SUCCESS(f'Done. Uploaded {uploaded} files.'))
