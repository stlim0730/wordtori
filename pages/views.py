from django.shortcuts import render
from django.db import models
from django.db.models import Q
from api.forms import SubmissionForm
from api.models import Submission, Category
from tagging.models import Tag
import base64

def getAllCategories():
  return Category.objects.filter(hidden=False)

def getAllSubmissions(category):
  submissions = Submission.objects.filter(
    Q(mediaHash__isnull=False) | Q(mediaType='image'),
    category__slug=category, published=True, consented=True,
    mediaType__isnull=False
  ).order_by('-submissionDate', 'name')
  for submission in submissions:
    submission.photo = base64.b64encode(submission.photo).decode('utf-8')
    if submission.mediaType == 'image':
      submission.blobContent = base64.b64encode(submission.blobContent).decode('utf-8')
  # TODO: Drop unused fields for performance
  return submissions

def categories(request):
  context = {
    'active': 'see',
    'categories': getAllCategories()
  }
  return render(request, 'categories.html', context)

def see(request, slug):
  submissions = getAllSubmissions(slug)
  tags = []
  for submission in submissions:
    t = [tag.name for tag in Tag.objects.get_for_object(submission)]
    tags.extend(t)
  context = {
    'active': 'see',
    'categories': getAllCategories(),
    'category': getAllCategories().filter(slug=slug)[0],
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
    'categories': getAllCategories,
    'form': SubmissionForm()
  }
  return render(request, 'speak.html', context)
