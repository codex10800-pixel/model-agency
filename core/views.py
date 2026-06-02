from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ModelProfile, PortfolioImage, ActorProfile
from .forms import ApplicationForm, ContactForm


# Home View
def home(request):
    featured_models = ModelProfile.objects.filter(is_featured=True)[:6]

    # Models split by category
    models_women = ModelProfile.objects.filter(category='women')[:6]
    models_men = ModelProfile.objects.filter(category='men')[:6]
    models_youth = ModelProfile.objects.filter(category='youth')[:6]

    # Actors split by category
    actors_women = ActorProfile.objects.filter(category='women')[:6]
    actors_men = ActorProfile.objects.filter(category='men')[:6]
    actors_youth = ActorProfile.objects.filter(category='youth')[:6]

    context = {
        'featured_models': featured_models,
        'models_women': models_women,
        'models_men': models_men,
        'models_youth': models_youth,
        'actors_women': actors_women,
        'actors_men': actors_men,
        'actors_youth': actors_youth,
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
        qs = ModelProfile.objects.all().order_by('-created_at')
        category = self.request.GET.get('category')
        if category in ('women', 'men', 'youth'):
            qs = qs.filter(category=category)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', '')
        context['current_category'] = category
        return context


class ActorsListView(ListView):
    model = ActorProfile
    template_name = 'core/actors.html'
    context_object_name = 'actors'
    paginate_by = 9

    def get_queryset(self):
        qs = ActorProfile.objects.all().order_by('-created_at')
        category = self.request.GET.get('category')
        if category in ('women', 'men', 'youth'):
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', '')
        context['current_category'] = category
        return context


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


def actor_detail(request, pk):
    actor = get_object_or_404(ActorProfile, pk=pk)
    portfolio_images = actor.portfolio_images.all()
    related_actors = ActorProfile.objects.exclude(pk=pk).order_by('-created_at')[:4]
    context = {
        'actor': actor,
        'portfolio_images': portfolio_images,
        'related_actors': related_actors,
    }
    return render(request, 'core/actor_detail.html', context)


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
    actors = ActorProfile.objects.all()
    context = {
        'models': models,
        'actors': actors,
    }
    return render(request, 'core/hire.html', context)
