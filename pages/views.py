from django.shortcuts import render
from django.db import models
from api.forms import SubmissionForm
from api.models import Submission, Category
import base64

def categories(request):
  context = {
    'active': 'see',
    'categories': Category.objects.filter(hidden=False)
  }
  return render(request, 'categories.html', context)

def see(request, slug):
  submissions = Submission.objects.filter(
    category__slug=slug, published=True, consented=True,
    mediaType__isnull=False, mediaHash__isnull=False
  )
  for submission in submissions:
    submission.photo = base64.b64encode(submission.photo).decode('utf-8')
  context = {
    'active': 'see',
    'category': Category.objects.filter(slug=slug)[0],
    'submissions': submissions
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
