from datetime import datetime
from .models import Title, Page
from .serializers import PageSerializer, TitleSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
import base64

def backupAll(key):
  rawData = {
    'titles': Title.objects.all(),
    'pages': Page.objects.all()
  }
  serializers = {
    'titles': TitleSerializer,
    'pages': PageSerializer
  }
  suffix = '' # For debugging purpose
  fileName = 'api/management/commands/{}{}{}'.format(key, suffix, '.json')
  outputList = []
  for d in rawData[key]:
    serialized = serializers[key](d).data
    outputList.append(serialized)
  with open(fileName, 'w', encoding='utf-8') as f:
    f.write(json.dumps(outputList, sort_keys=True, indent=2))

@receiver(post_save, sender=Page)
def pageUpdated(sender, instance, created, **kwargs):
  backupAll('pages')

@receiver(post_save, sender=Title)
def titleUpdated(sender, instance, created, **kwargs):
  backupAll('titles')

@receiver(post_delete, sender=Page)
def pageRemoved(sender, instance, **kwargs):
  backupAll('pages')

@receiver(post_delete, sender=Title)
def titleRemoved(sender, instance, **kwargs):
  backupAll('titles')
