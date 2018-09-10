from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from .forms import SubmissionForm
from .models import Submission
from django.shortcuts import render, redirect

# Create your views here.
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, ))
def upload(request):
  name = request.data['name']
  submissionMode = request.data['submissionMode']
  file = None
  if 'file' in request.FILES:
    file = request.FILES['file']
  url = request.data['url']
  description = request.data['description']
  if submissionMode == 'upload':
    if not file:
      # File size limit exceeded
      context = {
        'active': 'submit',
        'form': SubmissionForm()
      }
      return render(request, 'submit.html', context=context)
    blobContent = file.read()
    mimeType = file.content_type
    mediaType = mimeType.split('/')[0]
    submission = Submission(
      name=name,
      blobContent=blobContent,
      description=description,
      mimeType=mimeType,
      mediaType=mediaType
    )
    submission.save()
    context = {
      'active': 'submit',
      'form': SubmissionForm()
    }
    return render(request, 'submit.html', context=context)
  elif submissionMode == 'link':
    pass
  elif submissionMode == 'record':
    pass
  return Response({
    'mediaType': mediaType
  })
