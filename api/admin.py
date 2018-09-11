from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Submission
import base64
import tempfile
import os
from django.conf import settings

class SubmissionAdmin(admin.ModelAdmin):
  model = Submission
  list_display = ('submissionId', 'published', 'name', 'submissionDate', 'mediaType')
  readonly_fields = ['url', 'mimeType', 'mediaType', 'mediaHash', 'preview']

  def preview(self, obj):
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

admin.site.register(Submission, SubmissionAdmin)
