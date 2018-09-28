from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^media/upload$', views.upload, name='upload'),
  url(r'^media/play/(?P<category>[0-9]+)/(?P<submission>[0-9]+)$', views.play, name='play'),
]
