from django import forms
from .models import DownloadModel


class DownloadForm(forms.ModelForm):
    class Meta:
        model = DownloadModel
        exclude = ['name']
