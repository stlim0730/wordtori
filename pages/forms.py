from django import forms
from api.models import Submission

class SubmissionForm(forms.ModelForm):
  class Meta:
    model = Submission
    fields = ['name', 'description', 'url']

  name = forms.CharField(
    max_length=100,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Required'
      }
    )
  )
  # blobContent = models.BinaryField(null=True)
  url = forms.URLField(
    max_length=300, required=False,
    widget=forms.URLInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Link to YouTube or SoundCloud is supported.'
      }
    )
  )
  description = forms.CharField(
    required=False,
    widget=forms.Textarea(
      attrs={
        'class': 'form-control no-resize',
        'placeholder': 'Optional'
      }
    )
  )
  # MEDIA_TYPE_CHOICES
