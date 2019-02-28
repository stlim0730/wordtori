from datetime import datetime
from .models import Title, Page
from .serializers import PageSerializer, TitleSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
import base64
from django.conf import settings
import shlex, subprocess

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
  # Push changes to GitHub
  # git config user.email "<email_address>"
  # git config user.name "<human_readable_name>"
  # git add <target_file>
  # git commit -m "<auto-generated commit message>"
  # git push origin <branch>
  # stdin: <GitHub_ID>
  # stdin: <GitHub_password>
  if settings.DEBUG and settings.GITHUB_ACCOUNT and settings.GITHUB_PASSWORD and settings.EMAIL_ADDRESS and settings.NAME:
    subprocess.run('git config user.email "{}"'.format(settings.EMAIL_ADDRESS))
    subprocess.run('git config user.name "{}"'.format(settings.NAME))
    subprocess.run('git add {}'.format(fileName))
    subprocess.run('git add {}'.format('api/management/commands/*.html'))
    subprocess.run('git commit -m "{}"'.format('update data for {} model instances'.format(key)))
    pushProcess = subprocess.Popen(
      shlex.split('git push origin master'), cwd=settings.BASE_DIR,
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    pushProcess.communicate(settings.GITHUB_ACCOUNT)
    pushProcess.communicate(settings.GITHUB_PASSWORD)
    
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
