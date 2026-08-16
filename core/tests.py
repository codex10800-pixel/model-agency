from django.test import Client, TestCase
from django.urls import reverse

from core.forms import ApplicationForm
from core.models import ModelProfile, ActorProfile, Application


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

    def test_application_form_saves_application_type(self):
        form = ApplicationForm(data={
            'name': 'Test Applicant',
            'age': 23,
            'email': 'applicant@example.com',
            'phone': '+27123456789',
            'location': 'Cape Town',
            'application_type': 'actor',
            'experience': 'Some experience in runway and commercial work.',
        })

        self.assertTrue(form.is_valid(), form.errors)
        application = form.save()

        self.assertEqual(application.application_type, 'actor')
        self.assertTrue(Application.objects.filter(pk=application.pk).exists())

    def test_apply_success_message_includes_application_type(self):
        client = Client()
        response = client.post(
            reverse('apply'),
            {
                'name': 'Test Applicant',
                'age': 23,
                'email': 'applicant@example.com',
                'phone': '+27123456789',
                'location': 'Cape Town',
                'application_type': 'model',
                'experience': 'Some experience in runway and commercial work.',
            },
            secure=True,
            follow=True,
        )

        self.assertContains(response, 'Application submitted successfully for Model!')
