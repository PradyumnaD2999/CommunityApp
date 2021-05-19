# forms.py
from django import forms
from .models import *

class uploadImage(forms.ModelForm):
    class Meta:
        model = Profile1
        fields = ['image1']
