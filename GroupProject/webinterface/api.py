from rest_framework import generics, permissions

from .serializers import ProjectSerializer, AnalysisSerializer
from .models import Project, Analysis


class ProjectList(generics.ListCreateAPIView):
    model = Project
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class ProjectDetail(generics.RetrieveAPIView):
    model = Project
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'title'



class AnalysisList(generics.ListCreateAPIView):
    model = Analysis
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class AnalysisDetail(generics.RetrieveAPIView):
    model = Analysis
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()
    lookup_field = 'title'


#TODO get analysis from project
class ProjectAnalysisList(generics.RetrieveAPIView):
    model = Analysis
    serializer_class = AnalysisSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return Analysis.objects.filter(project_title=self.kwargs['title'])

