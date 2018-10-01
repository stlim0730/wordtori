from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SubmissionForm
from .models import Submission, Category, AdminEmail
from django.shortcuts import render, redirect
from tagging.models import Tag
import re
import urllib.request
from pages.views import getAllSubmissions
from django.db.models import Q
from .serializers import *

@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, ))
def upload(request):
  # For reseponse
  context = { 'active': 'speak', 'form': SubmissionForm(), 'categories': Category.objects.filter(hidden=False) }
  if request.data['consented'] != 'on':
    messages.add_message(request, messages.ERROR, 'Submission failed! Please check the consent form.')
    return render(request, 'speak.html', context=context)
  consented = True
  name = request.data['name']
  submissionMode = request.data['submissionMode']
  file = None
  if 'file' in request.FILES:
    file = request.FILES['file']
  url = request.data['url']
  description = request.data['description']
  yearsInNeighborhoodFrom = request.data['yearsInNeighborhoodFrom']
  yearsInNeighborhoodTo = request.data['yearsInNeighborhoodTo']
  yearOfBirth = request.data['yearOfBirth']
  placeOfBirth = request.data['placeOfBirth']
  occupations = request.data['occupations']
  photo = request.FILES['photo'].read()
  categoryId = request.data['categoryId']
  photoMimeType = request.FILES['photo'].content_type
  note = request.data['note']
  tags = request.data['tags']
  if submissionMode == 'upload':
    if not file:
      # File size limit exceeded or File not attached
      messages.add_message(request, messages.ERROR, 'Submission failed! Please check the attachment (upto 200MB).')
      return render(request, 'speak.html', context=context)
    blobContent = file.read()
    mimeType = file.content_type
    mediaType = mimeType.split('/')[0]
    submission = Submission(
      consented=consented,
      name=name,
      # Uploaded
      blobContent=blobContent,
      mimeType=mimeType,
      # Uploaded
      description=description,
      mediaType=mediaType,
      photo=photo,
      photoMimeType=photoMimeType,
      category=Category.objects.filter(categoryId=categoryId)[0],
      yearsInNeighborhoodFrom=yearsInNeighborhoodFrom,
      yearsInNeighborhoodTo=yearsInNeighborhoodTo,
      yearOfBirth=yearOfBirth,
      placeOfBirth=placeOfBirth,
      occupations=occupations,
      note=note
    )
    submission.save()
  elif submissionMode == 'link':
    # YouTube Link format: https://youtu.be/bSwga3LYLVg
    # SoundCloud Link format: https://soundcloud.com/user-28036692/thom-heyer
    # SoundCloud track id found in meta tag content="soundcloud://sounds:458282508"
    youTubeRegex = r'^https://youtu\.be/\w+$'
    soundCloudRegex = r'^https://soundcloud\.com/.+/.+$'
    mediaType = None
    mediaHash = None
    if re.match(youTubeRegex, url):
      mediaType = 'youtube'
      mediaHash = url.split('/')[-1]
    elif re.match(soundCloudRegex, url):
      scRes = urllib.request.urlopen(url)
      if scRes.status == 200:
        scCont = scRes.read().decode('utf-8')
        match = re.search(r'content=\"soundcloud://sounds:([0-9]+)\"', scCont)
        if match:
          mediaType = 'soundcloud'
          mediaHash = match.group(1)
        else:
          # The SoundCloud page is not reachable
          messages.add_message(request, messages.ERROR, 'Submission failed! Couldn\'t identify the content.')
          return render(request, 'speak.html', context=context)
      else:
        # The SoundCloud page is not reachable
        messages.add_message(request, messages.ERROR, 'Submission failed! The page doesn\'t exist.')
        return render(request, 'speak.html', context=context)
    else:
      # URL submission doesn't match the expected formats
      messages.add_message(request, messages.ERROR, 'Submission failed! Please check the URL (Links from SoundCloud or YouTube are accepted).')
      return render(request, 'speak.html', context=context)
    submission = Submission(
      consented=consented,
      name=name,
      # Linked
      url=url,
      mediaHash=mediaHash,
      # Linked
      description=description,
      mediaType=mediaType,
      photo=photo,
      photoMimeType=photoMimeType,
      category=Category.objects.filter(categoryId=categoryId)[0],
      yearsInNeighborhoodFrom=yearsInNeighborhoodFrom,
      yearsInNeighborhoodTo=yearsInNeighborhoodTo,
      yearOfBirth=yearOfBirth,
      placeOfBirth=placeOfBirth,
      occupations=occupations,
      note=note
    )
    submission.save()
  elif submissionMode == 'record':
    pass
  # Success
  Tag.objects.update_tags(submission, tags)
  messages.add_message(request, messages.SUCCESS, 'Successfully submitted! Your submission will be reviewed by the moderator.')
  adminEmails = [ae.email for ae in AdminEmail.objects.all()]
  if len(adminEmails) > 0:
    send_mail(
      'New Submission on WordToRI',
      'There is a new submission by {} on WordToRI. Review and publish the submission if it\'s appropriate.'.format(name),
      'no-reply@wordtori.com',
      adminEmails,
      fail_silently=True,
    )
  return render(request, 'speak.html', context=context)

@api_view(['GET'])
def play(request, category, submission):
  submission = Submission.objects.filter(category__categoryId=category, submissionId=submission)
  if len(submission) == 1:
    submission = submission[0]
    return Response({
      'name': submission.name,
      'yearsInNeighborhoodFrom': submission.yearsInNeighborhoodFrom,
      'yearsInNeighborhoodTo': submission.yearsInNeighborhoodTo,
      'yearOfBirth': submission.yearOfBirth,
      'placeOfBirth': submission.placeOfBirth,
      'occupations': submission.occupations,
      'description': submission.description,
      'tags': [t.name for t in submission.tags],
      'submissionDate': submission.submissionDate,
      'mediaType': submission.mediaType,
      'mediaHash': submission.mediaHash
    })
  else:
    return Response({
      'error': 'Submission not found.'
    })

@api_view(['GET'])
def typeFilter(request, category, mediaType):
  submissions = getAllSubmissions(category)
  if mediaType == 'video':
    submissions = submissions.filter(
      Q(mediaType=mediaType) | Q(mediaType='youtube')
    )
  elif mediaType == 'audio':
    submissions = submissions.filter(
      Q(mediaType=mediaType) | Q(mediaType='soundcloud')
    )
  elif mediaType == 'image':
    submissions = submissions.filter(mediaType=mediaType)
  submissionIds = [s.submissionId for s in submissions]
  return Response({
    'submissionIds': submissionIds
  })
