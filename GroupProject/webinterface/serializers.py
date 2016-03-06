from rest_framework import serializers
from .models import *



class TurbineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turbine
        fields = ('name', 'manufacturer', 'model', 'diameter', 'hub_height', 'bins', 'powerInKillowats', 'oneMeterStrip')
        lookup_field = 'name'


class ProjectSerializer(serializers.ModelSerializer):

    #turbines = serializers.StringRelatedField(many=False)

    class Meta:
        model = Project
        fields = ('title', 'date_created', 'date_updated', 'site_calibration_allowed', 'turbine')
        lookup_field = 'title'

    # Adding the TurbineSerializer allows us to get model when using Foriegn Key / or other related key field
    # Remember to add var to fields, when accessing in template - turbine.name etc;
    turbine = TurbineSerializer()




class AnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysis
        fields = ('title', 'date_created', 'date_updated', 'project')
        lookup_field = 'title'


