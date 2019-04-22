from django.shortcuts import render
from django.template import loader
from django.core import serializers
# from django.http import HttpResponse
from django.db.models import Q
from api.forms import SubmissionForm
from api.models import Submission, Category, Event, TermsOfConsent, Map
# from api.views import getSubIdsByTagPerCat
from pages.models import Title, Page
from tagging.models import Tag, TaggedItem
import json
import base64
from django.contrib import messages
from django.template.defaultfilters import register

@register.filter(name='dict_key')
def dict_key(d, k):
  return d[k]

def getTitle():
  title = list(Title.objects.all())[0].title
  return title

def getMenu():
  pages = list(Page.objects.all().order_by('pageOrder'))
  return pages

def getMapConfig():
  mapConfig = list(Map.objects.all())#[0]
  if len(mapConfig) > 0:
    return mapConfig[0]
  else:
    None

def getAllCategories():
  return Category.objects.filter(hidden=False)

def getSubmissionsPerCat(category):
  submissions = Submission.objects.filter(
    Q(mediaHash__isnull=False) | Q(mediaType='image'),
    # Q(mediaType='youtube') | Q(mediaType='soundcloud'),
    category__slug=category, published=True, consented=True
  ).order_by('-submissionDate', 'interviewer_name')
  for submission in submissions:
    submission.photo = base64.b64encode(submission.photo).decode('utf-8') if submission.photo else ''
    if submission.mediaType == 'image':
      submission.blobContent = base64.b64encode(submission.blobContent).decode('utf-8')
  return submissions

def getSubIdsByTagPerCat(category, tag):
  submissions = getSubmissionsPerCat(category)
  submissions = TaggedItem.objects.get_by_model(submissions, [tag])
  return [s.submissionId for s in submissions]

def getAllEvents():
  events = Event.objects.filter(hidden=False).order_by('-date', 'time')
  for event in events:
    if event.image:
      event.image = base64.b64encode(event.image).decode('utf-8')
  return events

def getSubmissionContext(slug=None):
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
  return {
    'title': getTitle(),
    'menu': getMenu(),
    'categories': categories,
    'category': category,
    'submissionCnt': submissionCnt,
    'submissions': submissions,
    'tags': sorted(list(set(tags)))
  }

def what(request, tag=None):
  context = getSubmissionContext()
  context['active'] = 'home'
  filtered = []
  if tag:
    categories = getAllCategories()
    for cat in categories:
      filtered.extend(getSubIdsByTagPerCat(cat.slug, tag))
  context = getSubmissionContext()
  context['active'] = 'home'
  context['filtered'] = filtered
  context['tag'] = tag
  return render(request, 'what.html', context)

def staticPage(request):
  oldLabel = request.path[1:-1]
  content = Page.objects.filter(oldLabel=oldLabel)[0].htmlContent
  context = {
    'title': getTitle(),
    'menu': getMenu(),
    'active': oldLabel,
    'staticContent': content
  }
  return render(request, 'base.html', context)

def map(request, slug=None):
  context = getSubmissionContext()
  mapConfig = getMapConfig()
  context['viewCenterLat'] = mapConfig.viewCenterLat if mapConfig else None
  context['viewCenterLong'] = mapConfig.viewCenterLong if mapConfig else None
  context['viewCenterZoom'] = mapConfig.viewCenterZoom if mapConfig else None
  context['active'] = 'map'
  context['submissionsForMap'] = []
  context['popups'] = []
  for cat in  context['submissions']:
    subPerCat = context['submissions'][cat]
    for s in subPerCat:
      context['submissionsForMap'].append({
        'categoryId': s.category.categoryId,
        'submissionId': s.submissionId,
        'name': s.interviewer_name,
        'latitude': float(s.latitude) if s.latitude else None,
        'longitude': float(s.longitude) if s.longitude else None,
        'photo': s.photo
      })
      context['popups'].append({
        'categoryId': s.category.categoryId,
        'submissionId': s.submissionId,
        'name': s.interviewer_name,
        'photo': s.photo
      })
  context['submissionsForMap'] = json.dumps(context['submissionsForMap'])
    # context['submissionsForMap'][cat] = serializers.serialize('json', context['submissions'][cat])
  return render(request, 'map.html', context)

def events(request):
  context = {
    'title': getTitle(),
    'menu': getMenu(),
    'active': 'events',
    'events': getAllEvents()
  }
  return render(request, 'events.html', context)

def speak(request):
  context = {
    'title': getTitle(),
    'menu': getMenu(),
    'active': 'speak',
    'categories': getAllCategories,
    'form': SubmissionForm(),
    'termsOfConsent': TermsOfConsent.objects.all()[0]
  }
  if 'record' in request.GET and request.GET['record']=='success':
    messages.add_message(request, messages.SUCCESS, 'Successfully submitted! Your submission will be reviewed by the moderator.')
  return render(request, 'speak.html', context)
