from rest_framework import serializers

from .models import Project, Analysis


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'date_created', 'date_updated', 'site_calibration_allowed')
        lookup_field = 'title'


class AnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysis
        fields = ('title', 'date_created', 'date_updated', 'project')
        lookup_field = 'title'


