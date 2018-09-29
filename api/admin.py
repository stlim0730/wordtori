from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Submission, Category, AdminEmail
import base64
import tempfile
import os
from django.conf import settings
from slugify import slugify

class SubmissionAdmin(admin.ModelAdmin):
  model = Submission
  list_display = ['submissionId', 'published', 'name', 'category', 'submissionDate', 'mediaType']
  readonly_fields = ['photoReview', 'photoMimeType', 'mimeType', 'review', 'consented', 'submissionDate']

  def photoReview(self, obj):
    photoFileExt = obj.photoMimeType.split('/')[-1]
    photoFileName = '{id}_{name}.{ext}'.format(
      id = obj.submissionId,
      name = slugify(obj.name),
      ext = photoFileExt
    )
    photoFilePath = os.path.join(settings.MEDIA_ROOT, photoFileName)
    with open(photoFilePath, 'wb') as fo:
      fo.write(obj.photo)
      return mark_safe('\
        <img src="/media/{fileName}" style="max-width: 500px" />'.format(fileName = photoFileName)
      )

  def review(self, obj):
    if obj.mimeType and obj.blobContent:
      # Uploaded media
      tempFileExt = obj.mimeType.split('/')[-1]
      tempFileName = '{id}_{name}.{ext}'.format(
        id = obj.submissionId,
        name = obj.name,
        ext = tempFileExt
      )
      tempFilePath = os.path.join(settings.MEDIA_ROOT, tempFileName)
      with open(tempFilePath, 'wb') as fo:
        fo.write(obj.blobContent)
        return mark_safe('\
          <a href="/media/{fileName}" target="_blank">Download to review</a>'.format(fileName = tempFileName)
        )
    elif obj.mediaType == 'youtube' and obj.mediaHash:
      return mark_safe('\
        <iframe width="533" height="300"\
          src="https://www.youtube.com/embed/{hash}"\
          frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>\
        </iframe>'.format(hash = obj.mediaHash)
      )
    elif obj.mediaType == 'soundcloud':
      return mark_safe('\
        <iframe \
          height="300" scrolling="no" frameborder="no" allow="autoplay"\
          src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{hash}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true">\
        </iframe>'.format(hash = obj.mediaHash)
      )

class CategoryAdmin(admin.ModelAdmin):
  model = Category
  list_display = ('categoryId', 'name', 'slug', 'hidden')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AdminEmail)
