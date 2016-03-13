from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Project, Turbine, Analysis
from .serializer import ProjectSerializer, TurbineSerializer, AnalysisSerializer
from django.shortcuts import get_object_or_404
from windAnalysis.dummy_analysis import dummy


def index(request):
    return render(request, 'base.html')


class TurbineViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = Turbine.objects.all()
    serializer_class = TurbineSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        print(serializer)

        turbine = Turbine.objects.get(name=request.data['turbine']['name'])

        if turbine:
            if serializer.is_valid():
                print(serializer.validated_data)
                Project.objects.create(turbine=turbine, **serializer.validated_data)
                return Response()

        print(serializer.errors)
        return Response()


class AnalysisViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        print(serializer)

        project = Project.objects.get(title=request.data['project']['title'])

        if project:
            if serializer.is_valid():
                print(serializer.validated_data)
                Analysis.objects.create(project=project, **serializer.validated_data)
                dummy()
                return Response()


        print(serializer.errors)
        return Response()

    def list(self, request, title=None):
        analysis = Analysis.objects.get(title=title)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

    def retrieve(self, request, title=None):
        project = Project.objects.get(title=title)
        serializer = AnalysisSerializer(Analysis.objects.filter(project=project), many=True)
        return Response(serializer.data)

