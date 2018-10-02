from django.shortcuts import render
from django.db import models
from api.forms import SubmissionForm
from api.models import Submission, Category
from tagging.models import Tag
import base64

def categories(request):
  context = {
    'active': 'see',
    'categories': Category.objects.filter(hidden=False)
  }
  return render(request, 'categories.html', context)

def getAllSubmissions(category):
  submissions = Submission.objects.filter(
    category__slug=category, published=True, consented=True,
    mediaType__isnull=False, mediaHash__isnull=False
  ).order_by('-submissionDate', 'name')
  for submission in submissions:
    submission.photo = base64.b64encode(submission.photo).decode('utf-8')
  # TODO: Drop unused fields for performance
  return submissions

def see(request, slug):
  submissions = getAllSubmissions(slug)
  tags = []
  for submission in submissions:
    t = [tag.name for tag in Tag.objects.get_for_object(submission)]
    tags.extend(t)
  context = {
    'active': 'see',
    'category': Category.objects.filter(slug=slug)[0],
    'submissions': submissions,
    'tags': sorted(list(set(tags)))
  }
  return render(request, 'see.html', context)

def why(request):
  context = { 'active': 'why' }
  return render(request, 'why.html', context)

def how(request):
  context = { 'active': 'how' }
  return render(request, 'how.html', context)

def groundrules(request):
  context = { 'active': 'groundrules' }
  return render(request, 'groundrules.html', context)

def speak(request):
  context = {
    'active': 'speak',
    'categories': Category.objects.filter(hidden=False),
    'form': SubmissionForm()
  }
  return render(request, 'speak.html', context)
