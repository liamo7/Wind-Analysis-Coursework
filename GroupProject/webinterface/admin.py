from django.contrib import admin
from .models import Project, Analysis, Turbine

# Register your models here.
admin.site.register(Project)
admin.site.register(Analysis)
admin.site.register(Turbine)
