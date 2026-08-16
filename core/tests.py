from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

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

    def test_application_upload_is_saved_as_a_viewable_url(self):
        client = Client()

        image = Image.new('RGB', (10, 10), color='blue')
        byte_array = BytesIO()
        image.save(byte_array, format='JPEG')
        upload = SimpleUploadedFile(
            'applicant-photo.jpg',
            byte_array.getvalue(),
            content_type='image/jpeg'
        )

        response = client.post(
            reverse('apply'),
            {
                'name': 'Upload Applicant',
                'age': 24,
                'email': 'upload@example.com',
                'phone': '+27123456789',
                'location': 'Durban',
                'application_type': 'actor',
                'experience': 'Experience in print and commercials.',
                'images': upload,
            },
            secure=True,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        application = Application.objects.filter(email='upload@example.com').latest('created_at')
        self.assertTrue(application.images)
        self.assertTrue(
            str(application.images.url).startswith('http') or '/media/' in str(application.images.url),
            f'Expected a public URL or media path, got: {application.images.url}'
        )
