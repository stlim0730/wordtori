from rest_framework import serializers
import base64

# class CategorySerializer(serializers.BaseSerializer):
#   def to_representation(self, obj):
#     return {
#       'categoryId': obj.categoryId,
#       'name': obj.name,
#       'slug': obj.slug,
#       'hidden': obj.hidden
#     }

# class SubmissionSerializer(serializers.BaseSerializer):
#   def to_representation(self, obj):
#     return {
#       'name': obj.name,
#       'yearsInNeighborhoodFrom': obj.yearsInNeighborhoodFrom,
#       'yearsInNeighborhoodTo': obj.yearsInNeighborhoodTo,
#       'yearOfBirth': obj.yearOfBirth,
#       'placeOfBirth': obj.placeOfBirth,
#       'occupations': obj.occupations,
#       'photo': base64.b64encode(obj.photo).decode('utf-8'),
#       'category': CategorySerializer(obj.category, many=False).data,
#       'consented': obj.consented,
#       'description': obj.description,
#       'note': obj.note,
#       'submissionId': obj.submissionId,
#       'submissionDate': obj.submissionDate,
#       'mediaType': obj.mediaType,
#       'mediaHash': obj.mediaHash,
#       'published': obj.published
#     }
