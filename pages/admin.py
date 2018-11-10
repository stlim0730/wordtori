from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
  model = Page
  list_display = ['pageId', 'pageOrder', 'label', 'oldLabel', 'usePageSettings']

admin.site.register(Page, PageAdmin)
