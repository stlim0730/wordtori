from django.db import models

class Title(models.Model):
  title = models.CharField(max_length=20, primary_key=True)

class Page(models.Model):
  pageId = models.AutoField(primary_key=True)
  pageOrder = models.IntegerField(null=True, default=0)
  label = models.CharField(max_length=20, unique=True)
  htmlContent = models.TextField(null=True, blank=True)
  oldLabel = models.CharField(max_length=len('groundrules'), unique=True)
  emphasized = models.BooleanField(default=False)
  usePageSettings = models.BooleanField(default=True)
  hiddenOnMenu = models.BooleanField(default=False)
  
  def __str__(self):
    return self.label + ' page'
