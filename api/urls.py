from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^media/upload$', views.upload, name='upload'),
]
