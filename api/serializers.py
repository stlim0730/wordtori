from rest_framework import serializers
import base64
from django.utils import timezone
import json

class CategorySerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'categoryId': obj.categoryId,
      'name': obj.name,
      'slug': obj.slug,
      'hidden': obj.hidden
    }

class SubmissionSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'narrator_name': obj.narrator_name if obj.narrator_name else None,
      'interviewer_name': obj.interviewer_name if obj.interviewer_name else None,
      'interview_date':  '{}-{:02d}-{:02d}'.format(
        obj.interview_date.year if obj.interview_date else timezone.now().year,
        obj.interview_date.month if obj.interview_date else timezone.now().month,
        obj.interview_date.day if obj.interview_date else timezone.now().day
      ),
      'interview_time':  '{}:{:02d}:{:02d}'.format(
        obj.interview_time.hour if obj.interview_time else timezone.now().hour,
        obj.interview_time.minute if obj.interview_time else timezone.now().minute,
        obj.interview_time.second if obj.interview_time else timezone.now().second
      ),
      'interview_location': obj.interview_location if obj.interview_location else None,
      'url': str(obj.url),
      'transcript': json.dumps(obj.transcript, indent=2) if obj.transcript else None,
      'summary': obj.summary if obj.summary else None,
      'hometown': obj.hometown if obj.hometown else None,
      'latitude': obj.latitude if obj.latitude else None,
      'longitude': obj.longitude if obj.longitude else None,
      'photo': base64.b64encode(obj.photo).decode('utf-8') if obj.photo else None,
      'tagline': obj.tagline if obj.tagline else None,
      'consented': obj.consented if obj.consented else None,
      'categoryId': obj.category.categoryId,
      'submissionId': obj.submissionId,
      'submissionDate': '{}-{:02d}-{:02d}'.format(
        obj.submissionDate.year if obj.submissionDate else timezone.now().year,
        obj.submissionDate.month if obj.submissionDate else timezone.now().month,
        obj.submissionDate.day if obj.submissionDate else timezone.now().day
      ),
      'photoMimeType': 'image/jpeg',
      'mediaType': obj.mediaType if obj.mediaType else None,
      'mediaHash': obj.mediaHash if obj.mediaHash else None,
      'published': obj.published
    }

class TermsOfConsentsSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'passage': obj.passage
    }

class AdminEmailSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'email': obj.email
    }

class EventSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'eventId': obj.eventId,
      'title': obj.title,
      'date': '{}-{:02d}-{:02d}'.format(
        obj.date.year,
        obj.date.month,
        obj.date.day
      ) if obj.date else None,
      'time': '{:02d}:{:02d}:{:02d}'.format(
        obj.time.hour,
        obj.time.minute,
        obj.time.second
      ) if obj.time else None,
      'location': obj.location if obj.location else None,
      'description': obj.description if obj.description else None,
      'link1': obj.link1 if obj.link1 else None,
      'link2': obj.link2 if obj.link2 else None,
      'videoURL': obj.videoURL if obj.videoURL else None,
      'mediaHash': obj.mediaHash if obj.mediaHash else None,
      'image': base64.b64encode(obj.image).decode('utf-8') if obj.image else None,
      'imageMimeType': 'image/jpeg',
      'hidden': obj.hidden
    }
