from datetime import datetime
from .models import Submission, Category, Event, AdminEmail, TermsOfConsent
from .serializers import SubmissionSerializer, CategorySerializer, EventSerializer, TermsOfConsentsSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
import base64

def backupAll(key):
  rawData = {
    'termsOfConsents': TermsOfConsent.objects.all(),
    'submissions': Submission.objects.all(),
    'categories': Category.objects.all(),
    'events': Event.objects.all()
  }
  serializers = {
    'termsOfConsents': TermsOfConsentsSerializer,
    'submissions': SubmissionSerializer,
    'categories': CategorySerializer,
    'events': EventSerializer
  }
  suffix = '' # For debugging purpose
  fileName = 'api/management/commands/{}{}{}'.format(key, suffix, '.json')
  outputList = []
  for d in rawData[key]:
    serialized = serializers[key](d).data
    outputList.append(serialized)
  with open(fileName, 'w', encoding='utf-8') as f:
    f.write(json.dumps(outputList, sort_keys=True, indent=2))

@receiver(post_save, sender=Submission)
def submissionUpdated(sender, instance, created, **kwargs):
  backupAll('submissions')

@receiver(post_save, sender=Category)
def categoryUpdated(sender, instance, created, **kwargs):
  backupAll('categories')

@receiver(post_save, sender=Event)
def eventUpdated(sender, instance, created, **kwargs):
  backupAll('events')

@receiver(post_save, sender=TermsOfConsent)
def tocUpdated(sender, instance, created, **kwargs):
  backupAll('termsOfConsents')

@receiver(post_delete, sender=Submission)
def submissionRemoved(sender, instance, **kwargs):
  backupAll('submissions')

@receiver(post_delete, sender=Category)
def categoryRemoved(sender, instance, **kwargs):
  backupAll('categories')

@receiver(post_delete, sender=Event)
def eventRemoved(sender, instance, **kwargs):
  backupAll('events')

@receiver(post_delete, sender=TermsOfConsent)
def tocRemoved(sender, instance, **kwargs):
  backupAll('termsOfConsents')
