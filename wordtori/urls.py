from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from pages import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('home/', views.what),
  path('home/<tag>', views.what), # url(r'^see/(?P<slug>.*)$', views.see, name='see'),
  path('about/', views.staticPage),
  path('map/', views.map),
  path('map/<slug>', views.map),
  path('events/', views.events), # url(r'^events$', views.events, name='events'),
  path('speak/', views.speak), # url(r'^speak$', views.speak, name='speak'),
  path('api/', include('api.urls')), # url(r'^api/', ),
  path('', views.what), # url(r'^$', views.see, name='see'),
]
