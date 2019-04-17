from django.db import models
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

  name = models.CharField(max_length=100)
  yearsInNeighborhoodFrom = models.CharField(max_length=4, null=True, blank=True)
  yearsInNeighborhoodTo = models.CharField(max_length=4, null=True, blank=True)
  yearOfBirth = models.CharField(max_length=4, null=True, blank=True)
  placeOfBirth = models.CharField(max_length=100, null=True, blank=True)
  latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
  longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
  occupations = models.CharField(max_length=200, null=True, blank=True)
  photo = models.BinaryField(max_length=5 * 1024 * 1024, null=True, blank=True)
  category= models.ForeignKey('Category', on_delete=models.CASCADE)
  consented = models.BooleanField(default=False)
  note = models.TextField(null=True, blank=True)
  contact = models.CharField(max_length=100, null=True, blank=True)
  tagline = models.CharField(max_length=300, null=True, blank=True)
  
  blobContent = models.BinaryField(null=True, blank=True, max_length=200 * 1024 * 1024)
  url = models.URLField(max_length=300, null=True, blank=True)
  description = models.TextField(null=True, blank=True)

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(null=True, blank=True)
  photoMimeType = models.CharField(max_length=len('image/jpeg'), null=True, blank=True)
  mimeType = models.CharField(max_length=len('video/webm'), null=True, blank=True, default='')
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  published = models.BooleanField(default=False)

  def __str__(self):
    return 'Submission: ' + self.name + ' (' + str(self.submissionId) + ')'

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
  viewCenterLat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
  viewCenterLong = models.DecimalField(max_digits=9, decimal_places=6, null=True)
  viewCenterZoom = models.IntegerField(null=True)

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
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  image = models.BinaryField(max_length=10 * 1024 * 1024, null=True)
  imageFile = models.ImageField(upload_to='events', null=True, blank=True)
  imageMimeType = models.CharField(max_length=len('image/jpeg'), null=True, blank=True, default='')
  hidden = models.BooleanField(default=False)

  def __str__(self):
   return 'Event: ' + self.title

class TermsOfConsent(models.Model):
  defaultPassage = """
    The information and data (submission) provided using this form will be reviewed by the moderator. If you agree to submit, you are assumed to agree with the moderator's decision to publish your submission through WordToRI.
  """
  passage = models.TextField(default=defaultPassage.strip())
