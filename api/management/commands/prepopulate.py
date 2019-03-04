import os
import sys
import datetime
from django.conf import settings
from django.core.management import BaseCommand
from django.db import connection, transaction, router
from api.models import Submission, Category, TermsOfConsent, Event
from pages.models import Title, Page
import json
import base64

class Command(BaseCommand):

  def handle(self, *args, **options):
    categories = None
    submissions = None
    termsOfConsents = None
    pages = None

    # Category
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'categories.json')
    with open(filePath, encoding='utf-8') as f:
      categories = json.load(f)
    cnt = 0
    for category in categories:
      exists = Category.objects.filter(slug=category['slug'])
      if exists:
        continue
      newCatetory = Category.objects.create(
        name=category['name'], slug=category['slug'],
        categoryId=category['categoryId']
      )
      cnt += 1
    print('{cnt} category objects were created.'.format(cnt=cnt))
    if len(Category.objects.all()) < 1:
      print('No categories found.')
      sys.exit(1)
    if cnt > 0:
      self.updateAutoIncrement('api', Category, 'categoryId', cnt + 1)

    # Submission
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submissions.json')
    with open(filePath, encoding='utf-8') as f:
      submissions = json.load(f)
    cnt = 0
    for submission in submissions:
      category = Category.objects.get(categoryId=submission['categoryId'])
      exists = Submission.objects.filter(
        name=submission['name'], yearOfBirth=submission['yearOfBirth'],
        placeOfBirth=submission['placeOfBirth'], occupations=submission['occupations'],
        category=category
      )
      if exists:
        continue
      dateSplit = submission['submissionDate'].split('-')
      submissionDate = datetime.datetime(year=int(dateSplit[0]), month=int(dateSplit[1]), day=int(dateSplit[2]))
      newSubmission = Submission.objects.create(
        name=submission['name'],
        yearsInNeighborhoodFrom=submission['yearsInNeighborhoodFrom'],
        yearsInNeighborhoodTo=submission['yearsInNeighborhoodTo'],
        yearOfBirth=submission['yearOfBirth'],
        placeOfBirth=submission['placeOfBirth'],
        occupations=submission['occupations'],
        photo=base64.b64decode(submission['photo']),
        category=category,
        consented=submission['consented'],
        description=submission['description'],
        note=submission['note'],
        submissionId=submission['submissionId'],
        submissionDate=submissionDate,#submission['submissionDate'],
        photoMimeType=submission['photoMimeType'],
        mediaType=submission['mediaType'],
        mediaHash=submission['mediaHash'],
        published=submission['published']
      )
      cnt += 1
    print('{cnt} submission objects were created.'.format(cnt=cnt))
    if cnt > 0:
      self.updateAutoIncrement('api', Submission, 'submissionId', cnt + 1)

    # Event
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.json')
    with open(filePath, encoding='utf-8') as f:
      events = json.load(f)
    cnt = 0
    for event in events:
      exists = Event.objects.filter(
        eventId=event['eventId'], title=event['title']
      )
      if exists:
        continue
      dateSplit = event['date'].split('-')
      timeSplit = event['time'].split(':')
      date = datetime.datetime(year=int(dateSplit[0]), month=int(dateSplit[1]), day=int(dateSplit[2]))
      time = datetime.time(hour=int(timeSplit[0]), minute=int(timeSplit[1]), second=int(timeSplit[2]))
      newEvent = Event.objects.create(
        eventId=event['eventId'],
        title=event['title'],
        date=date,
        time=time,
        location=event['location'],
        description=event['description'],
        link1=event['link1'],
        link2=event['link2'],
        image=base64.b64decode(event['image']),
        imageMimeType=event['imageMimeType'],
        videoURL=event['videoURL'],
        mediaHash=event['mediaHash'],
        hidden=event['hidden']
      )
      cnt += 1
    print('{cnt} event objects were created.'.format(cnt=cnt))
    if cnt > 0:
      self.updateAutoIncrement('api', Event, 'eventId', cnt + 1)

    # TermsOfConsents
    cnt = TermsOfConsent.objects.count()
    if cnt < 1:
      filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'termsOfConsents.json')
      with open(filePath, encoding='utf-8') as f:
        termsOfConsents = json.load(f)
      newToc = TermsOfConsent.objects.create(
        passage=termsOfConsents[0]['passage']
      )
      cnt += 1
      print('{cnt} termsOfConsent objects were created.'.format(cnt=cnt))

    # Title
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'titles.json')
    with open(filePath, encoding='utf-8') as f:
      titles = json.load(f)
    cnt = 0
    for title in titles:
      exists = Title.objects.filter(title=title['title'])
      if exists:
        continue
      newTitle = Title.objects.create(
        title=title['title']
      )
      cnt += 1
    print('{cnt} title objects were created.'.format(cnt=cnt))
    
    # Pages
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages.json')
    with open(filePath, encoding='utf-8') as f:
      pages = json.load(f)
    cnt = 0
    for page in pages:
      exists = Page.objects.filter(label=page['label'])
      if exists:
        continue
      htmlContent = None
      if page['htmlContent']:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}.html'.format(page['oldLabel'])), encoding='utf-8') as f:
          htmlContent = f.read()
      newPage = Page.objects.create(
        pageOrder=page['pageOrder'], label=page['label'], htmlContent=htmlContent, hiddenOnMenu=page['hiddenOnMenu'],
        oldLabel=page['oldLabel'], emphasized=page['emphasized'], usePageSettings=page['usePageSettings']
      )
      cnt += 1
    print('{cnt} page objects were created.'.format(cnt=cnt))
    if cnt > 0:
      self.updateAutoIncrement('pages', Page, 'pageId', cnt + 1)

# api_category_categoryId_seq
# api_submission_submissionId_seq

  def updateAutoIncrement(self, app, model, idField, value):
    cursor = connection.cursor()
    _router = settings.DATABASES[router.db_for_write(model)]['NAME']
    alter_str = "ALTER sequence \"{app}_{model}_{idField}_seq\" RESTART WITH {value}".format(
      app=app, model=model.__name__.lower(), idField=idField, value=value
    )
    # alter_str = "ALTER table {}.{} 'AUTO_INCREMENT'={}".format(
    #   _router, model._meta.db_table, value
    # )
    cursor.execute(alter_str)
    # transaction.commit_unless_managed()
