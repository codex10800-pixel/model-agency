from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('models/', views.ModelsListView.as_view(), name='models'),
    path('models/<int:pk>/', views.model_detail, name='model_detail'),
    path('actors/', views.ActorsListView.as_view(), name='actors'),
    path('actors/<int:pk>/', views.actor_detail, name='actor_detail'),
    path('apply/', views.ApplyView.as_view(), name='apply'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('hire/', views.hire, name='hire'),
]