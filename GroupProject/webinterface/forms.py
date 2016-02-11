from django.forms import forms, ModelForm
from .models import Project, Analysis


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['title']
