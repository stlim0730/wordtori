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

  # Required fields
  name = models.CharField(max_length=100)
  yearsInNeighborhoodFrom = models.CharField(max_length=4, null=True, blank=True)
  yearsInNeighborhoodTo = models.CharField(max_length=4, null=True, blank=True)
  yearOfBirth = models.CharField(max_length=4, null=True, blank=True)
  placeOfBirth = models.CharField(max_length=100, null=True, blank=True)
  occupations = models.CharField(max_length=200, null=True, blank=True)
  photo = models.BinaryField(max_length=5 * 1024 * 1024, null=True, blank=True)
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
  adminEmailId = models.AutoField(primary_key=True)
  email = models.EmailField()

  def __str__(self):
   return 'Email: ' + self.email

class Event(models.Model):
  eventId = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  date = models.DateField(null=True, blank=True)
  time = models.TimeField(null=True, blank=True)
  location = models.CharField(max_length=300)
  description = models.TextField(null=True, blank=True)
  link1 = models.URLField(max_length=300, null=True, blank=True)
  link2 = models.URLField(max_length=300, null=True, blank=True)
  image = models.BinaryField(max_length=10 * 1024 * 1024, null=True)
  imageFile = models.ImageField(upload_to='events', null=True, blank=True)
  imageMimeType = models.CharField(max_length=len('image/jpeg'), null=True, blank=True, default='')
  hidden = models.BooleanField(default=False)

  def __str__(self):
   return 'Event: ' + self.title
