from .models import Project, Turbine, Analysis
from rest_framework import serializers


class TurbineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turbine
        fields = ('id', 'name', 'bin', 'powerInKillowats')

    def create(self, validated_data):
        print(validated_data)
        return Turbine.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):

    turbine = TurbineSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'turbine', 'mastFile')


class AnalysisSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = ('id', 'title', 'project')

