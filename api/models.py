from django.db import models
from django.contrib.postgres.fields import JSONField
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

  narrator_name = models.CharField(max_length=100, null=True, blank=True)
  interviewer_name = models.CharField(max_length=100)
  interview_date = models.DateField(null=True, blank=True)
  interview_time = models.TimeField(null=True, blank=True)
  interview_location = models.CharField(max_length=100, null=True, blank=True)
  url = models.URLField(max_length=300, null=True, blank=True)
  summary = models.TextField(null=True, blank=True)
  transcript = JSONField(null=True, blank=True, default=None)
  hometown = models.CharField(max_length=100, null=True, blank=True)
  latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default=None)
  longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default=None)
  photo = models.BinaryField(max_length=5 * 1024 * 1024, null=True, blank=True)
  category= models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
  # contact = models.CharField(max_length=100, null=True, blank=True)
  tagline = models.CharField(max_length=300, null=True, blank=True)
  consented = models.BooleanField(default=False)

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(null=True, blank=True)
  photoFile = models.ImageField(upload_to='photo', null=True, blank=True)
  photoMimeType = models.CharField(max_length=len('image/jpeg'), null=True, blank=True)
  mimeType = models.CharField(max_length=len('video/webm'), null=True, blank=True, default='')
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  published = models.BooleanField(default=False)

  def __str__(self):
    return 'Submission: ' + self.interviewer_name + ' (' + str(self.submissionId) + ')'

# Django Tagging
register(Submission)

class Category(models.Model):
  class Meta:
    verbose_name_plural = 'categories'

  categoryId = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True)
  hidden = models.BooleanField(default=False)
  description = models.TextField(null=True, blank=True, default='')

  def __str__(self):
    return 'Category: ' + self.name

class AdminEmail(models.Model):
  # adminEmailId = models.AutoField(primary_key=True)
  email = models.EmailField(primary_key=True)

  def __str__(self):
   return 'Email: ' + self.email

class Map(models.Model):
  viewCenterLat = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default=None)
  viewCenterLong = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default=None)
  viewCenterZoom = models.IntegerField(null=True, blank=True, default=None)

  def __str__(self):
   return 'Center latitude: ' + str(self.viewCenterLat)\
   + ' / Center longitude: ' + str(self.viewCenterLong)\
   + ' / Center zoom: ' + str(self.viewCenterZoom)

class Event(models.Model):
  eventId = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  date = models.DateField(null=True, blank=True)
  time = models.TimeField(null=True, blank=True)
  location = models.CharField(max_length=300)
  description = models.TextField(null=True, blank=True)
  link1 = models.URLField(max_length=300, null=True, blank=True)
  link2 = models.URLField(max_length=300, null=True, blank=True)
  videoURL = models.URLField(max_length=300, null=True, blank=True)
  image = models.BinaryField(max_length=10 * 1024 * 1024, null=True)
  
  # Generated fields
  imageFile = models.ImageField(upload_to='events', null=True, blank=True)
  imageMimeType = models.CharField(max_length=len('image/jpeg'), null=True, blank=True, default='')
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  hidden = models.BooleanField(default=False)

  def __str__(self):
   return 'Event: ' + self.title

class TermsOfConsent(models.Model):
  defaultPassage = """
    The information and data (submission) provided using this form will be reviewed by the moderator. If you agree to submit, you are assumed to agree with the moderator's decision to publish your submission through WordToRI.
  """
  passage = models.TextField(default=defaultPassage.strip())
