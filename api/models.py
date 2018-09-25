from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Submission(models.Model):
  MEDIA_TYPE_CHOICES = (
    ('image', 'Image'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('soundcloud', 'SoundCloud'),
    ('youtube', 'YouTube')
  )

  YEAR_VALIDATORS = [
    MinValueValidator(1900),
    MaxValueValidator(datetime.datetime.now().year)
  ]

  # Required fields
  name = models.CharField(max_length=100)
  yearsInNeighborhoodFrom = models.IntegerField(validators=YEAR_VALIDATORS)
  yearsInNeighborhoodTo = models.IntegerField(validators=YEAR_VALIDATORS)
  yearOfBirth = models.IntegerField(validators=YEAR_VALIDATORS)
  placeOfBirth = models.CharField(max_length=100)
  occupations = models.CharField(max_length=200)
  photo = models.BinaryField(max_length=5 * 1024 * 1024)
  consented = models.BooleanField(default=False)

  # Optional fields
  blobContent = models.BinaryField(null=True, blank=True, max_length=200 * 1024 * 1024)
  url = models.URLField(max_length=300, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  note = models.TextField(null=True, blank=True)
  # TODO: tags = None

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(auto_now_add=True)
  photoMimeType = models.CharField(max_length=len('image/jpeg'))
  mimeType = models.CharField(max_length=len('video/webm'), null=True, blank=True, default='')
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  published = models.BooleanField(default=False)
