from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
import csv
import io

from .models import ModelProfile, PortfolioImage, Application, ContactMessage, ActorProfile, ActorPortfolioImage


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    readonly_fields = ('image',)


class ActorPortfolioImageInline(admin.TabularInline):
    model = ActorPortfolioImage
    extra = 1
    readonly_fields = ('image',)


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [f.name for f in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in field_names])
    return response


def mark_as_featured(modeladmin, request, queryset):
    updated = queryset.update(is_featured=True)
    modeladmin.message_user(request, f'{updated} profiles marked as featured.')


@admin.register(ModelProfile)
class ModelProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'height', 'location', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'location', 'created_at')
    search_fields = ('name', 'location', 'bio')
    list_editable = ('is_featured',)
    inlines = [PortfolioImageInline]
    readonly_fields = ('created_at', 'updated_at')
    actions = [export_as_csv, mark_as_featured]
    change_list_template = 'admin/core/modelprofile_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='core_modelprofile_import_csv'),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file uploaded.')
                return redirect(reverse('admin:core_modelprofile_changelist'))
            try:
                data = csv_file.read().decode('utf-8')
            except Exception:
                data = csv_file.read().decode('latin-1')
            reader = csv.DictReader(io.StringIO(data))
            created = 0
            with transaction.atomic():
                for row in reader:
                    name = row.get('name') or row.get('title')
                    if not name:
                        continue
                    age = row.get('age')
                    try:
                        age = int(age) if age else 0
                    except ValueError:
                        age = 0
                    defaults = {
                        'bio': row.get('bio', '') or '',
                        'location': row.get('location', '') or '',
                        'height': row.get('height', '') or '',
                        'is_featured': str(row.get('is_featured', '')).lower() in ('1', 'true', 'yes'),
                        'category': row.get('category', 'women') or 'women',
                    }
                    obj, created_flag = ModelProfile.objects.get_or_create(name=name, defaults={**defaults, 'age': age})
                    if created_flag:
                        created += 1
            messages.success(request, f'Imported {created} model profiles.')
            return redirect(reverse('admin:core_modelprofile_changelist'))

        context = {'opts': self.model._meta}
        return render(request, 'admin/core/import_profiles.html', context)


@admin.register(ActorProfile)
class ActorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'height', 'location', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'location', 'created_at')
    search_fields = ('name', 'location', 'bio')
    list_editable = ('is_featured',)
    inlines = [ActorPortfolioImageInline]
    readonly_fields = ('created_at', 'updated_at')
    actions = [export_as_csv, mark_as_featured]
    change_list_template = 'admin/core/actorprofile_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='core_actorprofile_import_csv'),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file uploaded.')
                return redirect(reverse('admin:core_actorprofile_changelist'))
            try:
                data = csv_file.read().decode('utf-8')
            except Exception:
                data = csv_file.read().decode('latin-1')
            reader = csv.DictReader(io.StringIO(data))
            created = 0
            with transaction.atomic():
                for row in reader:
                    name = row.get('name') or row.get('title')
                    if not name:
                        continue
                    age = row.get('age')
                    try:
                        age = int(age) if age else 0
                    except ValueError:
                        age = 0
                    defaults = {
                        'bio': row.get('bio', '') or '',
                        'location': row.get('location', '') or '',
                        'height': row.get('height', '') or '',
                        'is_featured': str(row.get('is_featured', '')).lower() in ('1', 'true', 'yes'),
                        'category': row.get('category', 'women') or 'women',
                    }
                    obj, created_flag = ActorProfile.objects.get_or_create(name=name, defaults={**defaults, 'age': age})
                    if created_flag:
                        created += 1
            messages.success(request, f'Imported {created} actor profiles.')
            return redirect(reverse('admin:core_actorprofile_changelist'))

        context = {'opts': self.model._meta}
        return render(request, 'admin/core/import_profiles.html', context)


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
