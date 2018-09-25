from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from django.contrib import messages
from .forms import SubmissionForm
from .models import Submission
from django.shortcuts import render, redirect
import re
import urllib.request

# Create your views here.
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, ))
def upload(request):
  if request.data['consented'] != 'on':
    context = { 'active': 'submit', 'form': SubmissionForm() }
    messages.add_message(request, messages.ERROR, 'Submission failed! Please check the consent form.')
    return render(request, 'submit.html', context=context)
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
  photoMimeType = request.FILES['photo'].content_type
  note = request.data['note']
  if submissionMode == 'upload':
    if not file:
      # File size limit exceeded or File not attached
      context = { 'active': 'submit', 'form': SubmissionForm() }
      messages.add_message(request, messages.ERROR, 'Submission failed! Please check the attachment (upto 200MB).')
      return render(request, 'submit.html', context=context)
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
          context = { 'active': 'submit', 'form': SubmissionForm() }
          messages.add_message(request, messages.ERROR, 'Submission failed! Couldn\'t identify the content.')
          return render(request, 'submit.html', context=context)
      else:
        # The SoundCloud page is not reachable
        context = { 'active': 'submit', 'form': SubmissionForm() }
        messages.add_message(request, messages.ERROR, 'Submission failed! The page doesn\'t exist.')
        return render(request, 'submit.html', context=context)
    else:
      # URL submission doesn't match the expected formats
      context = { 'active': 'submit', 'form': SubmissionForm() }
      messages.add_message(request, messages.ERROR, 'Submission failed! Please check the URL (Links from SoundCloud or YouTube are accepted).')
      return render(request, 'submit.html', context=context)
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
  messages.add_message(request, messages.SUCCESS, 'Successfully submitted! Your submission will be reviewed by the moderator.')
  context = { 'active': 'submit', 'form': SubmissionForm() }
  return render(request, 'submit.html', context=context)
