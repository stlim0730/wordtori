import os
import sys
from datetime import datetime
from django.core.management import BaseCommand
from api.models import Submission, Category
import json
import base64

class Command(BaseCommand):

  def handle(self, *args, **options):
    categories = None
    submissions = None

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
      submissionDate = datetime(year=int(dateSplit[0]), month=int(dateSplit[1]), day=int(dateSplit[2]))
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
        submissionDate=submission['submissionDate'],
        photoMimeType=submission['photoMimeType'],
        mediaType=submission['mediaType'],
        mediaHash=submission['mediaHash'],
        published=submission['published']
      )
      cnt += 1
    print('{cnt} submission objects were created.'.format(cnt=cnt))
