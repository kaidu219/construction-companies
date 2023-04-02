from django.urls import path, re_path
from .views import index, contacts, about

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('contacts', contacts, name='contacts'),
]