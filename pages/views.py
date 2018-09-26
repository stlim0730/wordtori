from django.shortcuts import render
from django.db import models
from api.forms import SubmissionForm
from api.models import Category

def see(request):
  context = {
    'active': 'see'
  }
  return render(request, 'see.html', context)

def why(request):
  context = {
    'active': 'why'
  }
  return render(request, 'why.html', context)

def how(request):
  context = {
    'active': 'how'
  }
  return render(request, 'how.html', context)

def groundrules(request):
  context = {
    'active': 'groundrules'
  }
  return render(request, 'groundrules.html', context)

def speak(request):
  context = {
    'active': 'speak',
    'categories': Category.objects.filter(hidden=False),
    'form': SubmissionForm()
  }
  return render(request, 'speak.html', context)
