from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets, views
from .models import Project, Turbine, Analysis, Column, JsonDataFile
from .serializer import ProjectSerializer, TurbineSerializer, AnalysisSerializer, ColumnSerializer
from windAnalysis.dummy_analysis import dummy
from windAnalysis.ppaTypes import *
from windAnalysis.utility import synchroniseDataFiles
from webinterface.testData import getWindTestData, getLidarTestData, getPowerTestData
from django.contrib import messages
import json
from GroupProject.settings import MEDIA_ROOT
from .utils import PythonObjectEncoder, as_python_object
import pandas as pd
def index(request):
    return render(request, 'base.html')


def message(request, msg):
    return HttpResponse({"message": msg})


class LogCatViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        msg = messages.get_messages(request)
        list = []
        for m in msg:
            list.append(m)
        return JsonResponse(list)


class TurbineViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = Turbine.objects.all()
    serializer_class = TurbineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            turbine = Turbine.objects.create(**serializer.validated_data)
            turbine.addOneMetreHorizontalStripes()
            return Response()

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
                messages.add_message(request._request, messages.SUCCESS, 'Project has been created.')
                return Response(data={"success": "Project Created."})

        return Response()

    def update(self, request, *args, **kwargs):

        project = Project.objects.get(title=request.data['projectTitle'])

        files = []

        if 'siteCalibrationFile' in request.data:
            project.siteCalibrationFile = request.data['siteCalibrationFile']
            project.save()
            path = MEDIA_ROOT + '/' + project.title + '/sitecalibration/siteCalibration.txt'
            parse = pd.read_csv(path, sep='\t')
            valueDict = parse.to_dict()

            degree = list(valueDict['degree'].values())
            offset = list(valueDict['offset'].values())
            slope = list(valueDict['slope'].values())
            siteCalDict = {}

            for ss, elem in enumerate(degree):
                siteCalDict[str(elem)] = {}
                siteCalDict[str(elem)]['slope'] = slope[ss]
                siteCalDict[str(elem)]['offset'] = offset[ss]

            jsonData, created = JsonDataFile.objects.get_or_create(name='siteCalibration', jsonData=json.dumps(siteCalDict, cls=PythonObjectEncoder), projectID=project.id)
            project.siteCalibrationDict = jsonData
            project.save()

        if 'mastFile' in request.data:
            project.mastFile = request.data['mastFile']
            mastFile = project.addDatafile('mast.txt', project.directory + '/media/' + project.title + '/rawDataFiles/', FileType.METEO, columnSeparator='\t')
            project.save()

            data = json.loads(request.data['mastFileDict'])

            addDataToFile(mastFile, data, project)

            jsonDataFile = json.dumps(mastFile, cls=PythonObjectEncoder)

            mastFile.loadFromFile()
            mastFile.clean()
            files.append(mastFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="mastFile", jsonData=jsonDataFile, projectID=project.id)
            project.windDataFile = jFile
            project.save()

        if 'lidarFile' in request.data:
            project.lidarFile = request.data['lidarFile']
            project.save()

            lidarFile = project.addDatafile('lidar.txt', project.directory + '/media/' + project.title + '/rawDataFiles/',
                                FileType.LIDAR, columnSeparator='\t')

            data = json.loads(request.data['lidarFileDict'])

            addDataToFile(lidarFile, data, project)
            jsonDataFile = json.dumps(lidarFile, cls=PythonObjectEncoder)

            lidarFile.loadFromFile()
            lidarFile.clean()
            files.append(lidarFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="lidarFile", jsonData=jsonDataFile, projectID=project.id)
            project.lidarDataFile = jFile
            project.save()

        if 'powerFile' in request.data:
            project.powerFile = request.data['powerFile']
            project.save()
            powerFile = project.addDatafile('power.txt', project.directory + '/media/' + project.title + '/rawDataFiles/',
                            FileType.POWER, columnSeparator='\t')

            data = json.loads(request.data['powerFileDict'])
            addDataToFile(powerFile, data, project)
            jsonDataFile = json.dumps(powerFile, cls=PythonObjectEncoder)

            powerFile.loadFromFile()
            powerFile.clean()
            files.append(powerFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="powerFile", jsonData=jsonDataFile, projectID=project.id)
            project.powerDataFile = jFile
            project.save()

        project.save()


        if files:
            combinedFile = synchroniseDataFiles('dummy_data.txt', project.getCombinedFilePath(), files)
            combinedFile.saveToFile()

            jsonCombined = json.dumps(combinedFile, cls=PythonObjectEncoder)
            jFile, created = JsonDataFile.objects.get_or_create(name="combinedFile", jsonData=jsonCombined, projectID=project.id)
            project.combinedDataFile = jFile

        project.save()
        return Response()


class AnalysisViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        project = Project.objects.get(title=request.data['project']['title'])

        if project:
            if serializer.is_valid():
                Analysis.objects.create(project=project, **serializer.validated_data)

                files = []

                if project.windDataFile:
                    dataFile = JsonDataFile.objects.get(id=project.windDataFile.id)
                    files.append(json.loads(dataFile.jsonData, object_hook=as_python_object))

                if project.powerDataFile:
                    dataFile = JsonDataFile.objects.get(id=project.powerDataFile.id)
                    files.append(json.loads(dataFile.jsonData, object_hook=as_python_object))

                if project.lidarDataFile:
                    dataFile = JsonDataFile.objects.get(id=project.lidarDataFile.id)
                    files.append(json.loads(dataFile.jsonData, object_hook=as_python_object))

                if project.combinedDataFile:
                     dataFile = JsonDataFile.objects.get(id=project.combinedDataFile.id)
                     files.append(json.loads(dataFile.jsonData, object_hook=as_python_object))


                dummy(project, files)
                return Response()

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
        if key == 'colSets':
            print('colsets')
            dataFile.addColumnSet(**val)
        else:
            print(key)
            print(val)
            dataFile.addColumn(project=project, **val)





class JsonResponse(HttpResponse):
    def init__(self, data):
        content = json.dumps(data, indent=2, ensure_ascii=False)
        super(JsonResponse, self).__init__(content=content,mimetype='application/json; charset=utf8')


def getLogMessages(request):
    storage = messages.get_messages(request)
    data = []

    for message in storage:
        data.append({
            'message': message.message,
            'status': message.tags
        })

    return JsonResponse(data)