from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ModelProfile, PortfolioImage
from .forms import ApplicationForm, ContactForm


# Home View
def home(request):
    featured_models = ModelProfile.objects.filter(is_featured=True)[:6]
    all_models = ModelProfile.objects.all()[:4]
    context = {
        'featured_models': featured_models,
        'all_models': all_models,
    }
    return render(request, 'core/home.html', context)


# About View
def about(request):
    return render(request, 'core/about.html')


# Models List View with Pagination
class ModelsListView(ListView):
    model = ModelProfile
    template_name = 'core/models.html'
    context_object_name = 'models'
    paginate_by = 9

    def get_queryset(self):
        return ModelProfile.objects.all().order_by('-created_at')


# Model Detail View
def model_detail(request, pk):
    model = get_object_or_404(ModelProfile, pk=pk)
    portfolio_images = model.portfolio_images.all()
    related_models = ModelProfile.objects.exclude(pk=pk).order_by('-created_at')[:4]
    context = {
        'model': model,
        'portfolio_images': portfolio_images,
        'related_models': related_models,
    }
    return render(request, 'core/model_detail.html', context)


# Apply View
class ApplyView(FormView):
    template_name = 'core/apply.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('apply')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Application submitted successfully! We will contact you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# Contact View
class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Message sent successfully! We will get back to you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# Hire Talent View
def hire(request):
    models = ModelProfile.objects.all()
    context = {
        'models': models,
    }
    return render(request, 'core/hire.html', context)
