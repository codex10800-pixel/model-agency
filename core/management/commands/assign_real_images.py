from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File as DjangoFile
from django.db.models import Q
import os
import random

from core.models import ModelProfile, PortfolioImage, ActorProfile, ActorPortfolioImage


class Command(BaseCommand):
    help = 'Assign real images from static/images to ModelProfile and ActorProfile and create portfolio images.'

    def handle(self, *args, **options):
        static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        if not os.path.isdir(static_images_dir):
            self.stdout.write(self.style.ERROR(f'Static images dir not found: {static_images_dir}'))
            return

        all_images = [f for f in os.listdir(static_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.webp'))]
        # Exclude obvious branding files
        exclude = {'logo.png', 'logo.jpg'}
        images = [f for f in all_images if f not in exclude]

        if not images:
            self.stdout.write(self.style.ERROR('No candidate images in static/images to assign.'))
            return

        # Partition likely model/actor images (fallback to full list)
        model_pool = [f for f in images if 'model' in f.lower() or 'founder' in f.lower() or 'hero' in f.lower()] or images
        actor_pool = model_pool.copy()

        # Assign to ModelProfile without a profile image
        models = ModelProfile.objects.filter(Q(profile_image='') | Q(profile_image__isnull=True)).order_by('pk')
        self.stdout.write(f'Assigning images to {models.count()} models...')
        for m in models:
            src = random.choice(model_pool)
            src_path = os.path.join(static_images_dir, src)
            if not os.path.exists(src_path):
                continue
            with open(src_path, 'rb') as f:
                djf = DjangoFile(f)
                name = f'{m.pk}_{src}'
                m.profile_image.save(name, djf, save=True)

            # create 1-4 portfolio images for this model
            num_port = random.randint(1, 4)
            for i in range(num_port):
                psrc = random.choice(images)
                psrc_path = os.path.join(static_images_dir, psrc)
                if not os.path.exists(psrc_path):
                    continue
                with open(psrc_path, 'rb') as pf:
                    pdjf = DjangoFile(pf)
                    pname = f'model_{m.pk}_port_{i}_{psrc}'
                    pi = PortfolioImage(model=m)
                    pi.image.save(pname, pdjf, save=True)

        # Assign to ActorProfile
        actors = ActorProfile.objects.filter(Q(profile_image='') | Q(profile_image__isnull=True)).order_by('pk')
        self.stdout.write(f'Assigning images to {actors.count()} actors...')
        for a in actors:
            src = random.choice(actor_pool)
            src_path = os.path.join(static_images_dir, src)
            if not os.path.exists(src_path):
                continue
            with open(src_path, 'rb') as f:
                djf = DjangoFile(f)
                name = f'{a.pk}_{src}'
                a.profile_image.save(name, djf, save=True)

            # create 1-3 portfolio images for this actor
            num_port = random.randint(1, 3)
            for i in range(num_port):
                psrc = random.choice(images)
                psrc_path = os.path.join(static_images_dir, psrc)
                if not os.path.exists(psrc_path):
                    continue
                with open(psrc_path, 'rb') as pf:
                    pdjf = DjangoFile(pf)
                    pname = f'actor_{a.pk}_port_{i}_{psrc}'
                    api = ActorPortfolioImage(actor=a)
                    api.image.save(pname, pdjf, save=True)

        self.stdout.write(self.style.SUCCESS('Assigned images and generated portfolio items.'))
