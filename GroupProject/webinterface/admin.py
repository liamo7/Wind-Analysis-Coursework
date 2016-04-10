from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Turbine)
admin.site.register(Analysis)
admin.site.register(Column)
admin.site.register(JsonDataFile)