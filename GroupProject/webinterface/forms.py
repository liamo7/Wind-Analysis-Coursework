from django import forms
from .models import Project, Analysis


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title']


class UploadFileForm(forms.Form):
    file = forms.FileField(label='select a file', required=False)