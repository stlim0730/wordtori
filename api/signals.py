from datetime import datetime
from .models import Submission, Category, AdminEmail, Event, TermsOfConsent
from .serializers import SubmissionSerializer, CategorySerializer, AdminEmailSerializer, EventSerializer, TermsOfConsentsSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
import base64

def backupAll():
  rawData = {
    'termsOfConsents': TermsOfConsent.objects.all(),
    'submissions': Submission.objects.all(),
    'categories': Category.objects.all()
  }
  serializers = {
    'termsOfConsents': TermsOfConsentsSerializer,
    'submissions': SubmissionSerializer,
    'categories': CategorySerializer
  }
  suffix = ''
  for key in rawData:
    fileName = 'api/management/commands/{}{}{}'.format(key, suffix, '.json')
    outputList = []
    for d in rawData[key]:
      serialized = serializers[key](d).data
      outputList.append(serialized)
    with open(fileName, 'w', encoding='utf-8') as f:
      f.write(json.dumps(outputList, sort_keys=True, indent=2))

  # adminEmails = AdminEmail.objects.all()
  # events = Event.objects.all()

@receiver(post_save, sender=Submission)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=AdminEmail)
@receiver(post_save, sender=Event)
@receiver(post_save, sender=TermsOfConsent)
def backupAllInstances(sender, instance, created, **kwargs):
  backupAll()

@receiver(post_delete, sender=Submission)
@receiver(post_delete, sender=Category)
@receiver(post_delete, sender=AdminEmail)
@receiver(post_delete, sender=Event)
@receiver(post_delete, sender=TermsOfConsent)
def backupAllInstances(sender, instance, **kwargs):
  backupAll()
