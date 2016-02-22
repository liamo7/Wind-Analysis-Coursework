from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProjectSerializer, AnalysisSerializer
from .models import Project, Analysis


class ProjectList(viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, title=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class AnalysisList(viewsets.ModelViewSet):
    model = Analysis
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request):
        queryset = Analysis.objects.all()
        serializer = AnalysisSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Analysis.objects.all()
        analysis = get_object_or_404(queryset, title=pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)


class ProjectAnalysisList(viewsets.ModelViewSet):
    model = Analysis
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project.objects.all(), title=pk)
        serializer = AnalysisSerializer(Analysis.objects.filter(project=project), many=True)
        return Response(serializer.data)

