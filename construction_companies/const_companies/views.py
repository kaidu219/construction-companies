from django.shortcuts import render
from .utils import *

# Create your views here.

def index(request):
    return render(request, 'const_companies/index.html')

def about(request):
    return render(request, 'const_companies/about.html')

def contacts(request):
    return render(request, 'const_companies/contacts.html')