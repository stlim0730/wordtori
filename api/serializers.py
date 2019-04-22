from rest_framework import serializers
import base64
from django.utils import timezone

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
      'categoryId': obj.category.categoryId,
      'consented': obj.consented,
      'description': obj.description if obj.description else None,
      'mediaHash': obj.mediaHash if obj.mediaHash else None,
      'mediaType': obj.mediaType if obj.mediaType else None,
      'name': obj.name if obj.name else None,
      'note': obj.note if obj.note else None,
      'occupations': obj.occupations if obj.occupations else None,
      'photo': base64.b64encode(obj.photo).decode('utf-8') if obj.photo else None,
      'photoMimeType': 'image/jpeg',
      'placeOfBirth': obj.placeOfBirth if obj.placeOfBirth else None,
      'published': obj.published,
      'submissionDate': '{}-{:02d}-{:02d}'.format(
        obj.submissionDate.year if obj.submissionDate else timezone.now().year,
        obj.submissionDate.month if obj.submissionDate else timezone.now().month,
        obj.submissionDate.day if obj.submissionDate else timezone.now().day
      ),
      'submissionId': obj.submissionId,
      'url': None,
      'yearOfBirth': obj.yearOfBirth if obj.yearOfBirth else None,
      'yearsInNeighborhoodFrom': obj.yearsInNeighborhoodFrom if obj.yearsInNeighborhoodFrom else None,
      'yearsInNeighborhoodTo': obj.yearsInNeighborhoodTo if obj.yearsInNeighborhoodTo else None
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
