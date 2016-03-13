from django.contrib import admin
from .models import Project, Turbine, Analysis

admin.site.register(Project)
admin.site.register(Turbine)
admin.site.register(Analysis)