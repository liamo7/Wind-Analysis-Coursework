from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, views
from .models import Project, Turbine, Analysis, Column, Datafile
from .serializer import ProjectSerializer, TurbineSerializer, AnalysisSerializer, ColumnSerializer
from windAnalysis.dummy_analysis import dummy
from windAnalysis.ppaTypes import *
import jsonpickle
from windAnalysis.utility import synchroniseDataFiles
from webinterface.testData import getWindTestData, getLidarTestData, getPowerTestData
import json
from .datamodel import TestData
from .utils import PythonObjectEncoder, as_python_object


def index(request):
    return render(request, 'base.html')


class TurbineViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = Turbine.objects.all()
    serializer_class = TurbineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(serializer)

        if serializer.is_valid():
            print(serializer.validated_data)
            turbine = Turbine.objects.create(**serializer.validated_data)
            turbine.addOneMetreHorizontalStripes()
            return Response()

        print(serializer.errors)
        return Response()


class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    #parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        turbine = Turbine.objects.get(name=request.data['turbine']['name'])

        if turbine:
            if serializer.is_valid():
                project = Project.objects.create(turbine=turbine, **serializer.validated_data)
                project.save()

                print("Project setup complete")
                return Response(data={"success": "Project Created."})

        print(serializer.errors)
        return Response()

    def update(self, request, *args, **kwargs):

        project = Project.objects.get(title=request.data['projectTitle'])

        files = []

        if 'mastFile' in request.data:
            project.mastFile = request.data['mastFile']
            mastFile = project.addDatafile('mast.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/', FileType.METEO, columnSeparator='\t')
            project.save()
            data = getWindTestData()

            addDataToFile(mastFile, data, project)
            jsonDataFile = json.dumps(mastFile, cls=PythonObjectEncoder)

            mastFile.loadFromFile()
            mastFile.clean()
            files.append(mastFile)

            project.windDataFile = jsonDataFile
            project.save()

        if 'lidarFile' in request.data:
            project.lidarFile = request.data['lidarFile']
            lidarFile = project.addDatafile('lidar.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/',
                                FileType.LIDAR, columnSeparator='\t')
            data = getLidarTestData()

            addDataToFile(lidarFile, data, project)
            jsonDataFile = json.dumps(lidarFile, cls=PythonObjectEncoder)

            lidarFile.loadFromFile()
            lidarFile.clean()
            files.append(lidarFile)

            project.lidarDataFile = jsonDataFile
            project.save()

        if 'powerFile' in request.data:
            project.powerFile = request.data['powerFile']
            powerFile = project.addDatafile('power.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/',
                            FileType.POWER, columnSeparator='\t')

            data = getPowerTestData()
            addDataToFile(powerFile, data, project)
            jsonDataFile = json.dumps(powerFile, cls=PythonObjectEncoder)

            powerFile.loadFromFile()
            powerFile.clean()
            files.append(powerFile)

            project.powerDataFile = jsonDataFile
            project.save()

        project.save()


        if files is not None:
            combinedFile = synchroniseDataFiles('dummy_data.txt', project.getCombinedFilePath(), files)
            combinedFile.saveToFile()

            jsonCombined = json.dumps(combinedFile, cls=PythonObjectEncoder)
            project.combinedDataFile = jsonCombined

        project.save()
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

                files = []

                if project.windDataFile:
                    files.append(json.loads(project.windDataFile, object_hook=as_python_object))

                if project.powerDataFile:
                    files.append(json.loads(project.powerDataFile, object_hook=as_python_object))

                if project.lidarDataFile:
                    files.append(json.loads(project.lidarDataFile, object_hook=as_python_object))

                if project.combinedDataFile:
                    files.append(json.loads(project.combinedDataFile, object_hook=as_python_object))


                dummy(project, files)
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


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class ColumnTypeViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        myList = []
        for colType in ColumnType:
            myList.append(colType.name)
        return Response(myList)

class ValueTypeViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        myList = []
        for valType in ValueType:
            myList.append(valType.name)
        return Response(myList)



def addDataToFile(dataFile, data, project):

    for key, val in data.items():
        if 'columnSet' in val:
            dataFile.addColumnSet(**val)
        else:
            dataFile.addColumn(project=project, **val)