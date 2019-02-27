from django.apps import AppConfig

class PagesConfig(AppConfig):
  name = 'pages'
  verbose_name = 'WordToRI Page Settings'
  
  # def ready(self):
  #   import pages.signals
