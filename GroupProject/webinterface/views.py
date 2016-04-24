from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, views
from .models import Project, Turbine, Analysis, Column, JsonDataFile
from .serializer import ProjectSerializer, TurbineSerializer, AnalysisSerializer, ColumnSerializer
from windAnalysis.ppaTypes import *
from windAnalysis.utility import synchroniseDataFiles
import json
from GroupProject.settings import MEDIA_ROOT
from .utils import PythonObjectEncoder, as_python_object, convertToSiteCalibrationDict
from django.core.exceptions import ObjectDoesNotExist
from .analysis import processAnalysis, postAnalysis

def index(request):
    return render(request, 'base.html')


class TurbineViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = Turbine.objects.all()
    serializer_class = TurbineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            turbine = Turbine.objects.create(**serializer.validated_data)
            turbine.addOneMetreHorizontalStripes()
            return Response(data={"success": "Turbine Created."})

        return Response(data={"error": serializer.errors['title'][0]})


@api_view(['POST'])
def getDataFile(request):

    if request.data['type'] == 'combined':
        try:
            jsonData = JsonDataFile.objects.get(name='combinedFile', projectID=request.data['dataID'])
            derivedFiles = JsonDataFile.objects.filter(name='derived', projectID=request.data['dataID'])
            print(derivedFiles)

            analysisNames = {}
            count=0
            for i in derivedFiles:
                analysisNames['derived' + str(count)] = Analysis.objects.get(id=i.analysisID).title
                count+=1

        except ObjectDoesNotExist:
            return Response(data={'error': 'Combined File does not exist.'})

        combinedFileCols = json.loads(jsonData.jsonData, object_hook=as_python_object)
        colList = [x.name for x in combinedFileCols.columns]
        return Response(data={'combinedFileCols': colList, 'derivedDataAnalyses': analysisNames})

    elif request.data['type'] == 'calculation':
        try:
            jsonData = JsonDataFile.objects.get(name='calculations', analysisID=request.data['dataID'])
        except ObjectDoesNotExist:
            return Response(data={'error': 'Calculations not set'})

        calcTable = jsonData.jsonData

        return Response(data={'calculationRows': jsonData.jsonData})



class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        turbine = Turbine.objects.get(name=request.data['turbine']['name'])

        if turbine:
            if serializer.is_valid():
                project = Project.objects.create(turbine=turbine, **serializer.validated_data)
                project.save()
                return Response(data={"success": "Project Created."})
        else:
            return Response(data={"error": "Not a valid turbine."})

        return Response(data={"error": serializer.errors['title'][0]})

    def update(self, request, *args, **kwargs):


        try:
            project = Project.objects.get(title=request.data['projectTitle'])
        except ObjectDoesNotExist:
            return Response(data={"error": "Project does not exist."})

        files = []

        if 'mastFile' in request.data:
            project.mastFile = request.data['mastFile']
            mastFile = project.addDatafile('mast.txt', project.directory + '/media/' + project.title + '/rawDataFiles/', FileType.METEO, columnSeparator='\t')
            project.save()

            data = json.loads(request.data['mastFileDict'])
            addDataToFile(mastFile, data, project)

            mastFile.loadFromFile()
            mastFile.clean()
            files.append(mastFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="mastFile", projectID=project.id)
            jFile.jsonData = json.dumps(mastFile, cls=PythonObjectEncoder)
            jFile.save()

            project.windDataFile = jFile
            project.save()

        if 'lidarFile' in request.data:
            project.lidarFile = request.data['lidarFile']
            project.save()

            lidarFile = project.addDatafile('lidar.txt', project.directory + '/media/' + project.title + '/rawDataFiles/',
                                FileType.LIDAR, columnSeparator='\t')

            data = json.loads(request.data['lidarFileDict'])

            addDataToFile(lidarFile, data, project)

            lidarFile.loadFromFile()
            lidarFile.clean()
            files.append(lidarFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="lidarFile", projectID=project.id)
            jFile.jsonData = json.dumps(lidarFile, cls=PythonObjectEncoder)
            jFile.save()

            project.lidarDataFile = jFile
            project.save()

        if 'powerFile' in request.data:
            project.powerFile = request.data['powerFile']
            project.save()
            powerFile = project.addDatafile('power.txt', project.directory + '/media/' + project.title + '/rawDataFiles/',
                            FileType.POWER, columnSeparator='\t')

            data = json.loads(request.data['powerFileDict'])
            addDataToFile(powerFile, data, project)

            powerFile.loadFromFile()
            powerFile.clean()
            files.append(powerFile)

            jFile, created = JsonDataFile.objects.get_or_create(name="powerFile", projectID=project.id)
            jFile.jsonData = json.dumps(powerFile, cls=PythonObjectEncoder)
            jFile.save()

            project.powerDataFile = jFile
            project.save()

        if 'siteCalibrationFile' in request.data and not files:
            project.siteCalibrationFile = request.data['siteCalibrationFile']
            project.save()
            path = MEDIA_ROOT + '/' + project.title + '/sitecalibration/siteCalibration.txt'
            siteCalData = convertToSiteCalibrationDict(path)

            jFile, created = JsonDataFile.objects.get_or_create(name='siteCalibration', projectID=project.id)
            jFile.jsonData = jsonData=json.dumps(siteCalData, cls=PythonObjectEncoder)
            jFile.save()

            project.siteCalibrationDict = jsonData
            project.save()
            return Response(data={"success": "Site Calibration file has been uploaded."})

        if files:
            combinedFile = synchroniseDataFiles('dummy_data.txt', project.getCombinedFilePath(), files)
            combinedFile.saveToFile()

            colList = [x.name for x in combinedFile.columns]

            jFile, created = JsonDataFile.objects.get_or_create(name="combinedFile", projectID=project.id)
            jFile.jsonData = json.dumps(combinedFile, cls=PythonObjectEncoder)
            jFile.save()

            project.combinedDataFile = jFile
            project.save()
            return Response(data={"success": "Project files have been uploaded.", "combinedCols": colList})

        project.save()
        return Response(data={"error": "No Data files have been loaded."})


class AnalysisViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            project = Project.objects.get(title=request.data['project']['title'])
        except ObjectDoesNotExist:
            return Response(data={"error": "Project does not exist."})

        calc = request.data['calculations']
        plotTypes = request.data['plotTypes']

        if project:
            if serializer.is_valid():

                analysis = Analysis.objects.create(project=project, **serializer.validated_data)

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

                if request.data['typeAnalysis'] == 'Synchronised':
                    # Create or replace the current table data for current analysis
                    tableCalcData, created = JsonDataFile.objects.get_or_create(name='calculations', analysisID=analysis.id)
                    tableCalcData.jsonData = calc
                    tableCalcData.save()

                    analysis.tableRows = tableCalcData
                    analysis.analysisType = 1
                    analysis.save()
                    processAnalysis(project, files, calc, analysis)
                    return Response(data={"success": "Analysis has been created"})


                else:
                    #Get derived file from analysis passed
                    dAnalysis = Analysis.objects.get(title=request.data['typeAnalysis'])
                    dataFile = JsonDataFile.objects.get(name='derived', analysisID=dAnalysis.id)


                    for plot in plotTypes:
                        if 'Distribution' in plotTypes[plot]['plotType']:
                            analysis.distributionPlot = True

                        if 'PowerCurve' in plotTypes[plot]['plotType']:
                            analysis.powerCurvePlot = True

                        if 'FFT' in plotTypes[plot]['plotType']:
                            analysis.fftPlot = True

                        if 'Correlation' in plotTypes[plot]['plotType']:
                            analysis.correlationPlot = True

                    analysis.analysisType = 2
                    response = postAnalysis(project, analysis, plotTypes, dataFile)
                    analysis.plotDict = response
                    analysis.save()
                    return Response(data={"success": "Analysis has been created", 'plotData': response})

        return Response(data={"error": serializer.errors})

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
            dataFile.addColumnSet(**val)
        else:
            dataFile.addColumn(project=project, **val)

