from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .projects import *

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

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            project = Project.objects.create(**serializer.validated_data)
            createProjectItem(project)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        # print("Error during creation of project")
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)


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

        if request.method == 'GET':
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

