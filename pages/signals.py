from datetime import datetime
from .models import Title, Page
from .serializers import PageSerializer, TitleSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
import base64
from django.conf import settings
import shlex, subprocess, shutil, os
from pathlib import Path

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
  if settings.DEBUG and settings.GITHUB_ACCOUNT and settings.GITHUB_PASSWORD and settings.EMAIL_ADDRESS:
    configPath = os.path.join(str(Path.home()), '.gitconfig')
    credPath = os.path.join(str(Path.home()), '.git-credentials')
    with open(configPath, 'w') as conf:
      conf.write('[credential]\n    helper = store')
    with open(credPath, 'w') as cred:
      cred.write('https://{}:{}@github.com'.format(settings.GITHUB_ACCOUNT, settings.GITHUB_PASSWORD))
    subprocess.run(
      shlex.split('git config user.email "{}"'.format(settings.EMAIL_ADDRESS)),
      cwd=settings.BASE_DIR
    )
    subprocess.run(
      shlex.split('git config user.name "{}"'.format(settings.GITHUB_ACCOUNT)),
      cwd=settings.BASE_DIR
    )
    subprocess.run(
      shlex.split('git add {}'.format(fileName)),
      cwd=settings.BASE_DIR
    )
    subprocess.run(
      shlex.split('git add {}'.format('api/management/commands/*.html')),
      cwd=settings.BASE_DIR
    )
    subprocess.run(
      shlex.split('git commit -m "{}"'.format('auto-update data for {} model instances'.format(key))),
      cwd=settings.BASE_DIR
    )
    subprocess.run(
      shlex.split('git push origin master'), cwd=settings.BASE_DIR
    )
    shutil.rmtree(configPath, ignore_errors=True)
    shutil.rmtree(credPath, ignore_errors=True)
    
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
