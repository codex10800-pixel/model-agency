from django.test import TestCase

from core.models import ModelProfile, ActorProfile


class MalformedImageFieldRegressionTests(TestCase):
    def test_model_profile_rejects_full_remote_url(self):
        profile = ModelProfile(
            name='Test Model',
            age=25,
            height='170cm',
            location='Cape Town',
            bio='bio',
            profile_image='https://res.cloudinary.com/test/image/upload/v123/file.jpg'
        )

        profile.save()

        self.assertEqual(str(profile.profile_image), '')

    def test_actor_profile_rejects_full_remote_url(self):
        actor = ActorProfile(
            name='Test Actor',
            age=28,
            height='175cm',
            location='Johannesburg',
            bio='bio',
            profile_image='https://res.cloudinary.com/test/image/upload/v123/file.jpg'
        )

        actor.save()

        self.assertEqual(str(actor.profile_image), '')
