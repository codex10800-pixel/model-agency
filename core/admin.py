from django.contrib import admin
from .models import ModelProfile, PortfolioImage, Application, ContactMessage


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    readonly_fields = ('image',)


@admin.register(ModelProfile)
class ModelProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'height', 'location', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'location', 'created_at')
    search_fields = ('name', 'location', 'bio')
    list_editable = ('is_featured',)
    inlines = [PortfolioImageInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'phone', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'email', 'phone', 'location')
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
