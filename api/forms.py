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
        'class': 'form-control'#,
        # 'placeholder': 'Required'
      }
    )
  )
  yearsInNeighborhoodFrom = forms.IntegerField(
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control mr-md-2',
        'placeholder': 'From'
      }
    )
  )
  yearsInNeighborhoodTo = forms.IntegerField(
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'To'
      }
    )
  )
  yearOfBirth = forms.IntegerField(
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  placeOfBirth = forms.CharField(
    max_length=100,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  occupations = forms.CharField(
    max_length=200,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  photo = forms.ImageField(
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control',
        'accept': 'image/*',
        'data-limit': 5
      }
    )
  )
  file = forms.FileField(
    required=False,
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control',
        'accept': 'audio/*,video/*,image/*',
        'data-limit': 200
      }
    )
  )
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
        'rows': '3',
        'class': 'form-control no-resize',
        'placeholder': 'Optional'
      }
    )
  )
  note = forms.CharField(
    required=False,
    widget=forms.Textarea(
      attrs={
        'rows': '2',
        'class': 'form-control no-resize',
        'placeholder': 'Optional'
      }
    )
  )
  consented = forms.BooleanField(
    widget=forms.CheckboxInput(
      attrs={
        'class': 'custom-control-input'
      }
    )
  )
