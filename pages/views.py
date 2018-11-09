from django.shortcuts import render
from django.db import models
from django.db.models import Q
from api.forms import SubmissionForm
from api.models import Submission, Category, Event
from tagging.models import Tag
import base64
from django.template.defaultfilters import register

@register.filter(name='dict_key')
def dict_key(d, k):
  return d[k]

def getAllCategories():
  return Category.objects.filter(hidden=False)

def getSubmissionsPerCat(category):
  submissions = Submission.objects.filter(
    Q(mediaHash__isnull=False) | Q(mediaType='image'),
    Q(mediaType='youtube') | Q(mediaType='soundcloud'),
    category__slug=category, published=True, consented=True
  ).order_by('-submissionDate', 'name')
  for submission in submissions:
    submission.photo = base64.b64encode(submission.photo).decode('utf-8')
    if submission.mediaType == 'image':
      submission.blobContent = base64.b64encode(submission.blobContent).decode('utf-8')
  # TODO: Drop unused fields for performance
  return submissions

def getAllEvents():
  events = Event.objects.filter(hidden=False).order_by('-date', 'time')
  for event in events:
    event.image = base64.b64encode(event.image).decode('utf-8')
  return events

def categories(request):
  context = {
    'active': 'see',
    'categories': getAllCategories()
  }
  return render(request, 'categories.html', context)

def see(request, slug=None):
  categories = getAllCategories()
  submissionCnt = {}
  for category in categories:
    submissionCnt[category.slug] = getSubmissionsPerCat(category.slug).count()
  submissions = {}
  if slug:
    categories = categories.filter(slug=slug)
  for category in categories:
    submissions[category.slug] = getSubmissionsPerCat(category.slug)
  tags = []
  for category in categories:
    for submission in submissions[category.slug]:
      t = [tag.name for tag in Tag.objects.get_for_object(submission)]
      tags.extend(t)
  categories = getAllCategories()
  for category in categories:
    if category.slug not in submissions:
      submissions[category.slug] = []
  context = {
    'active': 'see',
    'categories': categories,
    'submissionCnt': submissionCnt,
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

def events(request):
  context = {
    'active': 'events',
    'events': getAllEvents()
  }
  return render(request, 'events.html', context)

def speak(request):
  context = {
    'active': 'speak',
    'categories': getAllCategories,
    'form': SubmissionForm()
  }
  return render(request, 'speak.html', context)
