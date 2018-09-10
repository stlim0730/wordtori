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
  readonly_fields = ['mimeType', 'mediaType', 'preview']

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
          <a href="/media/{fileName}" target="_blank">Open in a New Tab</a>'.format(fileName = tempFileName)
        )
    else:
      return 'N/A'

admin.site.register(Submission, SubmissionAdmin)
