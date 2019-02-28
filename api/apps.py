from django.apps import AppConfig

class ApiConfig(AppConfig):
  name = 'api'
  verbose_name = 'WordToRI Submission Settings'
  
  def ready(self):
    import api.signals
