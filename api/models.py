from django.db import models

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

  # Optional fields
  blobContent = models.BinaryField(null=True, blank=True, max_length=200 * 1024 * 1024)
  url = models.URLField(max_length=300, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  # TODO: tags = None

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(auto_now_add=True)
  mimeType = models.CharField(max_length=len('video/webm'), null=True, blank=True, default='')
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  mediaHash = models.CharField(max_length=30, null=True, blank=True, default='')
  published = models.BooleanField(default=False)
