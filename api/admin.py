from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Submission, Category, AdminEmail, Event, TermsOfConsent
import base64
import tempfile
import os
import re
from tagging.models import Tag
import urllib.request
from django.conf import settings
from slugify import slugify
from django.contrib import messages

class SubmissionAdmin(admin.ModelAdmin):
  model = Submission
  list_display = ['submissionId', 'published', 'name', 'contact', 'category', 'submissionDate']
  readonly_fields = ['mediaType', 'mediaHash', 'photoReview', 'photoMimeType', 'mimeType', 'contentReview', 'consented', 'submissionDate']

  def save_model(self, request, obj, form, change):
    super(SubmissionAdmin, self).save_model(request, obj, form, change)
    # Handle tags
    Tag.objects.update_tags(obj, obj.tagline)
    # Handle blob content
    if obj.url and (obj.mediaType=='video' or obj.mediaType=='audio'):#'url' in form.changed_data:
      # 
      # This block of code is copied from api.view -- Keep them consistent
      # 
      youTubeRegex = r'^https://youtu\.be/.+$'
      soundCloudRegex = r'^https://soundcloud\.com/.+/.+$'
      mediaType = None
      mediaHash = None
      if re.match(youTubeRegex, obj.url):
        obj.mediaType = 'youtube'
        obj.mediaHash = obj.url.split('/')[-1]
        obj.blobContent = None
        obj.save()
        os.remove(self.getPhotoFilePath(obj))
        os.remove(self.getContentFilePath(obj))
      elif re.match(soundCloudRegex, obj.url):
        scRes = urllib.request.urlopen(obj.url)
        if scRes.status == 200:
          scCont = scRes.read().decode('utf-8')
          match = re.search(r'content=\"soundcloud://sounds:([0-9]+)\"', scCont)
          if match:
            obj.mediaType = 'soundcloud'
            obj.mediaHash = match.group(1)
            obj.blobContent = None
            obj.save()
            os.remove(self.getPhotoFilePath(obj))
            os.remove(self.getContentFilePath(obj))
          else:
            # The SoundCloud page is not reachable
            messages.add_message(request, messages.ERROR, 'Submission failed! Couldn\'t identify the content.')
        else:
          # The SoundCloud page is not reachable
          messages.add_message(request, messages.ERROR, 'Submission failed! The page doesn\'t exist.')
      else:
        # URL submission doesn't match the expected formats
        messages.add_message(request, messages.ERROR, 'Submission failed! Please check the URL (Links from SoundCloud or YouTube are accepted).')

  #     imageFilePath = None
  #     if obj.imageFile:
  #       imageFilePath = os.path.join(settings.MEDIA_ROOT, str(obj.imageFile))
  #       with open(imageFilePath, 'rb') as fi:
  #         obj.image = fi.read()
  #     super(EventAdmin, self).save_model(request, obj, form, change)
  #     if imageFilePath:
  #       os.remove(imageFilePath)

  def getPhotoFileName(self, obj):
    photoFileExt = obj.photoMimeType.split('/')[-1]
    return '{id}_{name}.{ext}'.format(
      id = obj.submissionId,
      name = slugify(obj.name),
      ext = photoFileExt
    )

  def getPhotoFilePath(self, obj):
    photoFileName = self.getPhotoFileName(obj)
    return os.path.join(settings.MEDIA_ROOT, 'photo', photoFileName)

  def getContentFileName(self, obj):
    contentFileExt = obj.mimeType.split('/')[-1]
    return '{id}_{name}.{ext}'.format(
      id = obj.submissionId,
      name = obj.name,
      ext = contentFileExt
    )

  def getContentFilePath(self, obj):
    contentFileName = self.getContentFileName(obj)
    return os.path.join(settings.MEDIA_ROOT, 'content', contentFileName)

  def photoReview(self, obj):
    photoFileName = self.getPhotoFileName(obj)
    photoFilePath = self.getPhotoFilePath(obj)
    with open(photoFilePath, 'wb') as fo:
      fo.write(obj.photo)
      return mark_safe('\
        <img src="/media/photo/{fileName}" style="max-width: 500px" />'.format(fileName = photoFileName)
      )

  def contentReview(self, obj):
    if obj.blobContent:# and obj.mimeType:
      # Uploaded media
      contentFileName = self.getContentFileName(obj)
      contentFilePath = self.getContentFilePath(obj)
      with open(contentFilePath, 'wb') as fo:
        fo.write(obj.blobContent)
        return mark_safe('\
          <a href="/media/content/{fileName}" target="_blank">Download to review</a>'.format(fileName = contentFileName)
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
  list_display = ['categoryId', 'name', 'slug', 'hidden']

class EventAdmin(admin.ModelAdmin):
  model = Event
  list_display = ['eventId', 'title', 'date', 'location', 'hidden']
  readonly_fields = ['imageMimeType', 'imageReview']

  def save_model(self, request, obj, form, change):
    super(EventAdmin, self).save_model(request, obj, form, change)
    if 'imageFile' in form.changed_data:
      imageFilePath = None
      if obj.imageFile:
        imageFilePath = os.path.join(settings.MEDIA_ROOT, str(obj.imageFile))
        with open(imageFilePath, 'rb') as fi:
          obj.image = fi.read()
      obj.save()
      if imageFilePath:
        os.remove(imageFilePath)

  def imageReview(self, obj):
    if obj.image:
      return mark_safe('\
          <img src="data:{imageMimeType};base64,{image}" style="max-width: 500px" />'
          .format(imageMimeType=obj.imageMimeType, image=base64.b64encode(obj.image).decode('utf-8'))
        )
    else:
      return None

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(AdminEmail)
admin.site.register(TermsOfConsent)
