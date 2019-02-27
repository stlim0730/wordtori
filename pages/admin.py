from django.contrib import admin
from .models import Title, Page

class TitleAdmin(admin.ModelAdmin):
  model = Title
  list_display = ['title']

admin.site.register(Title, TitleAdmin)

class PageAdmin(admin.ModelAdmin):
  model = Page
  list_display = ['pageId', 'pageOrder', 'label', 'oldLabel', 'usePageSettings']

admin.site.register(Page, PageAdmin)
