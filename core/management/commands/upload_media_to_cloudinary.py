from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import ModelProfile, ActorProfile, PortfolioImage, ActorPortfolioImage, Application
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Upload all local media files to Cloudinary and update database records'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting media upload to Cloudinary...\n'))
        
        # Verify Cloudinary is configured
        if not cloudinary.config().cloud_name:
            self.stdout.write(self.style.ERROR('ERROR: CLOUDINARY_URL not configured!'))
            return

        # Use local filesystem storage to access the files
        local_storage = FileSystemStorage(location=str(settings.MEDIA_ROOT))
        migrated_count = 0
        error_count = 0

        # Migrate ModelProfile images
        self.stdout.write('Processing ModelProfile images...')
        for profile in ModelProfile.objects.all():
            if profile.profile_image and not str(profile.profile_image).startswith('http'):
                try:
                    # Build the path manually
                    file_path = os.path.join(settings.MEDIA_ROOT, profile.profile_image.name)
                    if os.path.exists(file_path):
                        # Upload to Cloudinary
                        result = cloudinary.uploader.upload(
                            file_path,
                            folder='models/profile/',
                            resource_type='auto'
                        )
                        # Update the database with the Cloudinary URL
                        profile.profile_image = result['secure_url']
                        profile.save(update_fields=['profile_image'])
                        self.stdout.write(f'  ✅ {profile.name}: {result["secure_url"][:60]}...')
                        migrated_count += 1
                    else:
                        self.stdout.write(f'  ⚠️  {profile.name}: File not found at {file_path}')
                        error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ {profile.name}: {str(e)}'))
                    error_count += 1

        # Migrate ActorProfile images
        self.stdout.write('\nProcessing ActorProfile images...')
        for profile in ActorProfile.objects.all():
            if profile.profile_image and not str(profile.profile_image).startswith('http'):
                try:
                    file_path = os.path.join(settings.MEDIA_ROOT, profile.profile_image.name)
                    if os.path.exists(file_path):
                        result = cloudinary.uploader.upload(
                            file_path,
                            folder='actors/profile/',
                            resource_type='auto'
                        )
                        profile.profile_image = result['secure_url']
                        profile.save(update_fields=['profile_image'])
                        self.stdout.write(f'  ✅ {profile.name}: {result["secure_url"][:60]}...')
                        migrated_count += 1
                    else:
                        self.stdout.write(f'  ⚠️  {profile.name}: File not found')
                        error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ {profile.name}: {str(e)}'))
                    error_count += 1

        # Migrate PortfolioImage
        self.stdout.write('\nProcessing PortfolioImage images...')
        for portfolio in PortfolioImage.objects.all():
            if portfolio.image and not str(portfolio.image).startswith('http'):
                try:
                    file_path = os.path.join(settings.MEDIA_ROOT, portfolio.image.name)
                    if os.path.exists(file_path):
                        result = cloudinary.uploader.upload(
                            file_path,
                            folder='models/portfolio/',
                            resource_type='auto'
                        )
                        portfolio.image = result['secure_url']
                        portfolio.save(update_fields=['image'])
                        self.stdout.write(f'  ✅ {portfolio.model.name}: {result["secure_url"][:60]}...')
                        migrated_count += 1
                    else:
                        self.stdout.write(f'  ⚠️  {portfolio.model.name}: File not found')
                        error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ {portfolio.model.name}: {str(e)}'))
                    error_count += 1

        # Migrate ActorPortfolioImage
        self.stdout.write('\nProcessing ActorPortfolioImage images...')
        for portfolio in ActorPortfolioImage.objects.all():
            if portfolio.image and not str(portfolio.image).startswith('http'):
                try:
                    file_path = os.path.join(settings.MEDIA_ROOT, portfolio.image.name)
                    if os.path.exists(file_path):
                        result = cloudinary.uploader.upload(
                            file_path,
                            folder='actors/portfolio/',
                            resource_type='auto'
                        )
                        portfolio.image = result['secure_url']
                        portfolio.save(update_fields=['image'])
                        self.stdout.write(f'  ✅ {portfolio.actor.name}: {result["secure_url"][:60]}...')
                        migrated_count += 1
                    else:
                        self.stdout.write(f'  ⚠️  {portfolio.actor.name}: File not found')
                        error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ {portfolio.actor.name}: {str(e)}'))
                    error_count += 1

        # Migrate Application images
        self.stdout.write('\nProcessing Application images...')
        for app in Application.objects.all():
            if app.images and not str(app.images).startswith('http'):
                try:
                    file_path = os.path.join(settings.MEDIA_ROOT, app.images.name)
                    if os.path.exists(file_path):
                        result = cloudinary.uploader.upload(
                            file_path,
                            folder='applications/',
                            resource_type='auto'
                        )
                        app.images = result['secure_url']
                        app.save(update_fields=['images'])
                        self.stdout.write(f'  ✅ {app.name}: {result["secure_url"][:60]}...')
                        migrated_count += 1
                    else:
                        self.stdout.write(f'  ⚠️  {app.name}: File not found')
                        error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ {app.name}: {str(e)}'))
                    error_count += 1

        # Summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully migrated: {migrated_count}'))
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  Errors: {error_count}'))
        self.stdout.write('='*70 + '\n')
        
        self.stdout.write(self.style.SUCCESS('Upload complete! Run check_image_urls.py to verify.'))
