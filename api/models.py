from django.db import models

class Submission(models.Model):
  MEDIA_TYPE_CHOICES = (
    ('image', 'Image'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('soundcloud', 'Soundcloud'),
    ('youtube', 'Youtube')
  )
  
  # Required fields
  name = models.CharField(max_length=100)

  # Optional fields
  blobContent = models.BinaryField(null=True, blank=True)
  url = models.URLField(max_length=300, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  # TODO: tags = None

  # Generated fields
  submissionId = models.AutoField(primary_key=True)
  submissionDate = models.DateField(auto_now_add=True)
  mediaType = models.CharField(max_length=len('soundcloud'), choices=MEDIA_TYPE_CHOICES)
  embed = models.TextField(null=True)
  published = models.BooleanField(default=False)

# SoundCloud Embed format
# <iframe width="100%"
# height="300" scrolling="no" frameborder="no" allow="autoplay"
# src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/461240991&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

# YouTube Embed format
# <iframe width="560" height="315"
# src="https://www.youtube.com/embed/bSwga3LYLVg"
# frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
