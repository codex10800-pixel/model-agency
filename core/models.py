from django.db import models


# Shared category choices for models/actors
CATEGORY_CHOICES = [
    ('women', 'Women'),
    ('men', 'Men'),
    ('youth', 'Youth'),
]


class ModelProfile(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='women', db_index=True)
    age = models.PositiveIntegerField()
    height = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='models/profile/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class PortfolioImage(models.Model):
    model = models.ForeignKey(ModelProfile, related_name='portfolio_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='models/portfolio/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio for {self.model.name}"


class ActorProfile(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='women', db_index=True)
    age = models.PositiveIntegerField()
    height = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='actors/profile/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class ActorPortfolioImage(models.Model):
    actor = models.ForeignKey(ActorProfile, related_name='portfolio_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='actors/portfolio/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio for {self.actor.name}"


class Application(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    experience = models.TextField()
    images = models.ImageField(upload_to='applications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
