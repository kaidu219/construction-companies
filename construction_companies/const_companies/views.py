from django.shortcuts import render
from .utils import *

# Create your views here.

def index(request):
    return render(request, 'const_companies/index.html')

def about(request):
    capstroy = capstroy_parsing()
    context = {
        'capstroy': capstroy
    }
    return render(request, 'const_companies/about.html', context)

def contacts(request):
    capstroy = capstroy_parsing()
    context = {
        'capstroy': capstroy
    }
    return render(request, 'const_companies/contacts.html', context)