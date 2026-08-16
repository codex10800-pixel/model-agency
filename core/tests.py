from django.test import TestCase

from core.models import ModelProfile, ActorProfile


class CloudinaryRemoteUrlFieldTests(TestCase):
    def test_model_profile_accepts_full_remote_url(self):
        url = 'https://res.cloudinary.com/test/image/upload/v123/file.jpg'
        profile = ModelProfile(
            name='Test Model',
            age=25,
            height='170cm',
            location='Cape Town',
            bio='bio',
            profile_image=url
        )

        profile.save()

        self.assertEqual(profile.profile_image, url)

    def test_actor_profile_accepts_full_remote_url(self):
        url = 'https://res.cloudinary.com/test/image/upload/v123/file.jpg'
        actor = ActorProfile(
            name='Test Actor',
            age=28,
            height='175cm',
            location='Johannesburg',
            bio='bio',
            profile_image=url
        )

        actor.save()

        self.assertEqual(actor.profile_image, url)
