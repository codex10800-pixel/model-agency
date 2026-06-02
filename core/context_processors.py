from .models import ModelProfile, ActorProfile


def category_counts(request):
    """Provide counts per category for models and actors."""
    cats = ['women', 'men', 'youth']
    model_counts = {c: ModelProfile.objects.filter(category=c).count() for c in cats}
    actor_counts = {c: ActorProfile.objects.filter(category=c).count() for c in cats}
    model_counts['total'] = sum(model_counts.values())
    actor_counts['total'] = sum(actor_counts.values())
    return {
        'model_category_counts': model_counts,
        'actor_category_counts': actor_counts,
    }
