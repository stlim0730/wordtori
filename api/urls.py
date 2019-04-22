from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
  path('media/upload/', views.upload),
  path('media/play/<category>/<submission>/', views.play),# url(r'^media/play/(?P<category>[0-9]+)/(?P<submission>[0-9]+)$', views.play, name='play'),
  path('media/updateTag/<category>/<submission>/', views.updateTag),
  # path('media/filter/tag/<tag>/', views.filterBytag),
  # url(r'^media/filter/tag/(?P<category>.+)/(?P<tag>.+)/$', views.tagFilter),
  url(r'^media/search/(?P<category>.+)/(?P<keyword>.+)/$', views.searchFilter),
]
