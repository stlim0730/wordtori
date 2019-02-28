from rest_framework import serializers

class TitleSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    return {
      'title': obj.title
    }

class PageSerializer(serializers.BaseSerializer):
  def to_representation(self, obj):
    if obj.htmlContent:
      suffix = '' # For debugging purpose
      fileName = 'api/management/commands/{}{}.html'.format(obj.oldLabel, suffix)
      with open(fileName, 'w') as f:
        f.write(obj.htmlContent)
    return {
      'pageId': obj.pageId,
      'pageOrder': obj.pageOrder if obj.pageOrder else None,
      'label': obj.label,
      'htmlContent': obj.htmlContent if obj.htmlContent else None,
      'oldLabel': obj.oldLabel,
      'emphasized': obj.emphasized,
      'usePageSettings': obj.usePageSettings,
      'hiddenOnMenu': obj.hiddenOnMenu
    }
