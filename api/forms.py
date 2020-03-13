from django import forms
from api.models import Submission
import tagging

class SubmissionForm(forms.ModelForm):
  class Meta:
    model = Submission
    fields = [
      'name', 'yearsInNeighborhoodFrom', 'yearsInNeighborhoodTo',
      'yearOfBirth', 'placeOfBirth', 'occupations', 'category',
      'consented', 'url', 'description', 'note'
    ]
    
  name = forms.CharField(
    max_length=100,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Required'
      }
    )
  )
  contact = forms.CharField(
    max_length=100,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Email Address or Phone Number; this information won\'t be published'
      }
    )
  )
  yearsInNeighborhoodFrom = forms.IntegerField(
    required=False,
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control mr-md-2',
        'placeholder': 'From'
      }
    )
  )
  yearsInNeighborhoodTo = forms.IntegerField(
    required=False,
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'To'
      }
    )
  )
  yearOfBirth = forms.IntegerField(
    required=False,
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  placeOfBirth = forms.CharField(
    required=False,
    max_length=100,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  latitude = forms.DecimalField(
    required=False,
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Latitude'
      }
    )
  )
  longitude = forms.DecimalField(
    required=False,
    widget=forms.NumberInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Longitude'
      }
    )
  )
  occupations = forms.CharField(
    required=False,
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
    required=False,
    max_length=300,
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
        'class': 'form-control no-resize'
      }
    )
  )
  tags = tagging.forms.TagField(
    required=False,
    widget=forms.TextInput(
      attrs={
        'class': 'form-control'
      }
    )
  )
  note = forms.CharField(
    required=False,
    widget=forms.Textarea(
      attrs={
        'rows': '2',
        'class': 'form-control no-resize'
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
