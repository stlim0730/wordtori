from django.shortcuts import render
from .forms import SubmissionForm

def speak(request):
  context = {
    'active': 'speak'
  }
  return render(request, 'speak.html', context)

def why(request):
  context = {
    'active': 'why'
  }
  return render(request, 'why.html', context)

def how(request):
  context = {
    'active': 'how'
  }
  return render(request, 'how.html', context)

def groundrules(request):
  context = {
    'active': 'groundrules'
  }
  return render(request, 'groundrules.html', context)

def submit(request):
  context = {
    'active': 'submit',
    'form': SubmissionForm()
  }
  return render(request, 'submit.html', context)
