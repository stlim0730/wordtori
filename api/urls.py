from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^media/upload$', views.upload, name='upload'),
  url(r'^media/play/(?P<category>[0-9]+)/(?P<submission>[0-9]+)$', views.play, name='play'),
  url(r'^media/filter/type/(?P<category>.+)/(?P<mediaType>.+)$', views.typeFilter, name='typeFilter'),
  url(r'^media/filter/tag/(?P<category>.+)/(?P<tag>.+)$', views.tagFilter, name='tagFilter'),
]
