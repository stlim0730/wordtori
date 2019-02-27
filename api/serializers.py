from rest_framework import serializers
import base64

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
      'description': obj.description,
      'mediaHash': obj.mediaHash,
      'mediaType': obj.mediaType,
      'name': obj.name,
      'note': obj.note,
      'occupations': obj.occupations,
      'photo': base64.b64encode(obj.photo).decode('utf-8'),
      'photoMimeType': 'image/jpeg',
      'placeOfBirth': obj.placeOfBirth,
      'published': obj.published,
      'submissionDate': '{}-{:02d}-{:02d}'.format(
        obj.submissionDate.year,
        obj.submissionDate.month,
        obj.submissionDate.day
      ),
      'submissionId': obj.submissionId,
      'url': None,
      'yearOfBirth': obj.yearOfBirth,
      'yearsInNeighborhoodFrom': obj.yearsInNeighborhoodFrom,
      'yearsInNeighborhoodTo': obj.yearsInNeighborhoodTo
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
    pass
    return {
      'eventId': obj.eventId,
      'title': obj.title,
      'date': '{}-{:02d}-{:02d}'.format(
        obj.date.year,
        obj.date.month,
        obj.date.day
      ),
      'time': '{:02d}:{:02d}:{:02d}'.format(
        obj.time.hour,
        obj.time.minute,
        obj.time.second
      ),
      'location': obj.location,
      'description': obj.description,
      'link1': obj.link1,
      'link2': obj.link2,
      'videoURL': obj.videoURL,
      'mediaHash': obj.mediaHash,
      'image': base64.b64encode(obj.image).decode('utf-8'),
      'imageMimeType': 'image/jpeg',
      'hidden': obj.hidden
    }
