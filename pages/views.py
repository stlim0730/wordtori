from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# from django.db import models
from django.db.models import Q
from api.forms import SubmissionForm
from api.models import Submission, Category, Event
from pages.models import Page
from tagging.models import Tag
import base64
from django.contrib import messages
from django.template.defaultfilters import register

@register.filter(name='dict_key')
def dict_key(d, k):
  return d[k]

def getMenu():
  pages = list(Page.objects.all().order_by('pageOrder'))
  return pages

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

def see(request, slug=None):
  categories = getAllCategories()
  submissionCnt = {}
  for category in categories:
    submissionCnt[category.slug] = getSubmissionsPerCat(category.slug).count()
  submissions = {}
  category = None
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
  if slug:
    category = getAllCategories().filter(slug=slug)[0]
  else:
    category = None
  context = {
    'menu': getMenu(),
    'active': 'see',
    'categories': categories,
    'category': category,
    'submissionCnt': submissionCnt,
    'submissions': submissions,
    'tags': sorted(list(set(tags)))
  }
  return render(request, 'see.html', context)

def staticPage(request):
  oldLabel = request.path[1:]
  content = Page.objects.filter(oldLabel=oldLabel)[0].htmlContent
  context = {
    'menu': getMenu(),
    'active': oldLabel,
    'staticContent': content
  }
  return render(request, 'base.html', context)

def events(request):
  context = {
    'menu': getMenu(),
    'active': 'events',
    'events': getAllEvents()
  }
  return render(request, 'events.html', context)

def speak(request):
  context = {
    'menu': getMenu(),
    'active': 'speak',
    'categories': getAllCategories,
    'form': SubmissionForm()
  }
  if 'record' in request.GET and request.GET['record']=='success':
    messages.add_message(request, messages.SUCCESS, 'Successfully submitted! Your submission will be reviewed by the moderator.')
  return render(request, 'speak.html', context)
