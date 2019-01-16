from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from pages import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('see/', views.see),
  path('see/<slug>', views.see), # url(r'^see/(?P<slug>.*)$', views.see, name='see'),
  path('why/', views.staticPage), # url(r'^why$', views.staticPage, name='staticPage'),
  path('how/', views.staticPage), # url(r'^how$', views.staticPage, name='staticPage'),
  path('groundrules/', views.staticPage),
  path('events/', views.events), # url(r'^events$', views.events, name='events'),
  path('speak/', views.speak), # url(r'^speak$', views.speak, name='speak'),
  path('api/', include('api.urls')), # url(r'^api/', ),
  path('', views.see), # url(r'^$', views.see, name='see'),
]
