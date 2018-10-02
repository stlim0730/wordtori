from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from tagging.registry import register

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
  yearsInNeighborhoodFrom = models.IntegerField(validators=YEAR_VALIDATORS, null=True)
  yearsInNeighborhoodTo = models.IntegerField(validators=YEAR_VALIDATORS, null=True)
  yearOfBirth = models.IntegerField(validators=YEAR_VALIDATORS, null=True)
  placeOfBirth = models.CharField(max_length=100, null=True)
  occupations = models.CharField(max_length=200, null=True)
  photo = models.BinaryField(max_length=5 * 1024 * 1024, null=True)
  category= models.ForeignKey('Category', on_delete=models.CASCADE)
  consented = models.BooleanField(default=False)

  # Optional fields
  blobContent = models.BinaryField(null=True, blank=True, max_length=200 * 1024 * 1024)
  url = models.URLField(max_length=300, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  note = models.TextField(null=True, blank=True)
  # TODO: tags = None

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(default=datetime.datetime.now())
  photoMimeType = models.CharField(max_length=len('image/jpeg'), null=True)
  mimeType = models.CharField(max_length=len('video/webm'), null=True, blank=True, default='')
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  published = models.BooleanField(default=False)

# Django Tagging
register(Submission)

class Category(models.Model):
  class Meta:
    verbose_name_plural = 'categories'

  categoryId = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True)
  hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.name

class AdminEmail(models.Model):
  adminEmailId = models.AutoField(primary_key=True)
  email = models.EmailField()
  