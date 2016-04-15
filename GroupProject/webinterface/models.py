from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField, HStoreField
from windAnalysis.powerCurve import *
from math import pi
from enumfields import EnumField
from windAnalysis.ppaTypes import *
import pandas as pd
import numpy as np
import windAnalysis.calculation as calc
import operator as op
from inspect import signature
from windAnalysis.ppaTypes import *
import os as os
from GroupProject.settings import MEDIA_ROOT

class ProjectManager(models.Manager):

    def getLidarFilePath(self, fileName):
        return '{0}/rawDataFiles/lidar.txt'.format(self.title)

    def getMastFilePath(self, fileName):
        return '{0}/rawDataFiles/mast.txt'.format(self.title)

    def getPowerFilePath(self, fileName):
        return '{0}/rawDataFiles/power.txt'.format(self.title)

    def getSiteCalibrationFilePath(self, fileName):
        return '{0}/sitecalibration/siteCalibration.txt'.format(self.title)

    def getSynchronisedFilePath(self):
        return '{0}/synced/synchronisedData.txt'.format(self.title)

    def getCombinedFilePath(self):
        return '{0}/combined/'

class Turbine(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False)
    manufacturer = models.CharField(max_length=300, blank=True, null=True)
    model =models.CharField(max_length=300, blank=True, null=True)

    hubHeight = models.FloatField(blank=False, null=False, default=80)
    diameter = models.FloatField(blank=False, null=False, default=90)

    bin = ArrayField(models.FloatField(blank=True, null=True), blank=True, null=True)
    powerInKillowats = ArrayField(models.FloatField(blank=True, null=True), blank=True, null=True)

    # stripeArea = models.FloatField(blank=True, null=True)
    # proportion = models.FloatField(blank=True, null=True)
    # windSpeedHeight = models.FloatField(blank=True, null=True)

    stripes = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def radius(self):
        return self.diameter / 2

    def lowerTipHeight(self):
        return self.hubHeight - self.radius()

    def upperTipHeight(self):
        return self.hubHeight + self.radius()

    def sweptArea(self):
        return pi * pow(self.diameter / 2, 2)

    def getPowerCurveDict(self):
        return {'bin': self.bin, 'powerInKilowatts': self.powerInKillowats}

    def warrantedPowerCurve(self):
        return PowerCurve(self.getPowerCurveDict(), interpolate=True, warranted=True)

    def addOneMetreHorizontalStripes(self):

        self.list = []

        previousHeight = self.lowerTipHeight()
        diameterFraction = np.round(self.diameter % 1, 7)
        loopLimit = self.diameter
        if diameterFraction > 0:
            loopLimit = self.diameter - 1
            height = round(previousHeight + diameterFraction / 2, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction / 4, 7)
            self.list.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})

            previousHeight = height
        for i in np.arange(loopLimit):
            height = round(previousHeight + 1, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + 0.5, 7)
            self.list.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})
            previousHeight = height
        if diameterFraction > 0:
            height = round(previousHeight + diameterFraction / 2, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction / 4, 7)
            self.list.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})


        print(self.list)
        self.stripes = self.list
        self.save()
        print(self.stripes)

class JsonDataFile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    jsonData = JSONField(blank=True, null=True)

    projectID = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)
    description = models.TextField(max_length=3000, blank=True, null=True)
    turbine = models.ForeignKey(Turbine, related_name='turbine', null=True)
    directory = models.CharField(max_length=600, default=os.getcwd())

    siteCalibrationFile = models.FileField(upload_to=ProjectManager.getSiteCalibrationFilePath, null=True, blank=True)
    siteCalibrationDict = models.ForeignKey(JsonDataFile, null=True, blank=True, related_name="siteCalibrationDict", on_delete=models.CASCADE)

    windDataFile = models.ForeignKey(JsonDataFile, null=True, blank=True, related_name="windDataFile", on_delete=models.CASCADE)
    powerDataFile = models.ForeignKey(JsonDataFile, null=True, blank=True, related_name="powerDataFile", on_delete=models.CASCADE)
    lidarDataFile = models.ForeignKey(JsonDataFile, null=True, blank=True, related_name="lidarDataFile", on_delete=models.CASCADE)
    combinedDataFile = models.ForeignKey(JsonDataFile, null=True, blank=True, related_name="combinedDataFile", on_delete=models.CASCADE)

    mastFile = models.FileField(upload_to=ProjectManager.getMastFilePath, blank=True, null=True)
    lidarFile = models.FileField(upload_to=ProjectManager.getLidarFilePath, blank=True, null=True)
    powerFile = models.FileField(upload_to=ProjectManager.getPowerFilePath, blank=True, null=True)

    def __str__(self):
        return self.title

    def getCombinedFilePath(self):
        return MEDIA_ROOT + '/{0}/combined/'.format(self.title)

    def addDataFileNames(self, list):
        self.datafiles = list
        self.save()

    def addDatafile(self, name=None, containingDirectory=None, fileType=None, rowsToSkip=[], columnSeparator='\t', badDataValues=[]):
        return Datafile(name, containingDirectory, fileType, rowsToSkip, columnSeparator, badDataValues)

    def defineTurbine(self, turbine):
        self.turbine = turbine

    def stringifySiteCalibrationFactors(self):
        siteCalibrationFactorsAsStrings = {}
        for scf, value in self.siteCalibrationFactors.items():
            slope = str(value['slope'])
            offset = str(value['offset'])
            siteCalibrationFactorsAsStrings.update({str(scf): {'slope': slope, 'offset': offset}})
        return siteCalibrationFactorsAsStrings

    def deStringifySiteCalibrationFactors(self, factorDict):
        siteCalibrationFactorsDict = {}
        for scf, value in factorDict.items():
            slope = float(value['slope'])
            offset = float(value['offset'])
            siteCalibrationFactorsDict.update({int(scf): {'slope': slope, 'offset': offset}})
        return siteCalibrationFactorsDict

    def makeMeasuredPowerCurve(self, data, windSpeedColumn, powerColumn, binColumn, binWidth=0.5, airDensity=1.225):
        grouped = data.groupby(binColumn).aggregate({windSpeedColumn: 'mean',
                                                    powerColumn: 'mean',
                                                    binColumn: 'count'})
        grouped = grouped.rename(columns={binColumn: 'recordsPerBin', windSpeedColumn: 'meanWindSpeed', powerColumn: 'powerInKilowatts'})
        grouped['bin'] = grouped.index
        grouped['binStatus'] = BinStatus.EXCLUDED
        grouped.index = list(range(len(grouped)))

        powerCurve = PowerCurve(grouped.to_dict(orient='list'),
                                cutin=self.turbine.warrantedPowerCurve().cutin,
                                cutout=self.turbine.warrantedPowerCurve().cutout,
                                windSpeedStep=binWidth,
                                referenceAirDensity=airDensity)

        return powerCurve.validated().padded()


class Analysis(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)
    description = models.TextField(max_length=3000, blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return self.title


class Column(models.Model):
    name = models.CharField(max_length=300, blank=False)
    positionInFile = models.IntegerField(blank=True, null=True)
    columnType = EnumField(ColumnType)
    valueType = EnumField(ValueType)
    instrumentCalibrationSlope = models.FloatField(default=1.0)
    instrumentCalibrationOffset = models.FloatField(default=0.0)
    dataLoggerCalibrationSlope = models.FloatField(default=1.0)
    dataLoggerCalibrationOffset = models.FloatField(default=0.0)
    measurementHeight = models.FloatField(default=0.0)

    segmentWeighting = models.FloatField(blank=True, null=True)
    inferiorLimitHeight = models.FloatField(blank=True, null=True)
    superiorLimitHeight = models.FloatField(blank=True, null=True)
    segmentHeight = models.FloatField(blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.project is not None:
            return self.name + '(' + self.project.title + ')'
        else:
            return self.name


class Datafile(object):
    def __init__(self, name=None, containingDirectory=None, fileType=None, rowsToSkip=[], columnSeparator='\t', badDataValues=[]):
        self.filename = name
        self.directory = containingDirectory
        self.fileType = fileType
        self.columns = []
        self.columnSeparator = columnSeparator
        self.rowsToSkip = rowsToSkip
        self.columnSets = {}
        self.badDataValues = badDataValues
        self.selectors = []
        self.rewsLevels = {}
        #print("Datafile: " + self.filename)

    def fullyQualifiedPath(self):
        return self.directory + '/' + self.filename

    def addColumn(self, name, positionInFile, columnType, valueType,
                  instrumentCalibrationSlope=1.0, instrumentCalibrationOffset=0.0,
                  dataLoggerCalibrationSlope=1.0, dataLoggerCalibrationOffset=0.0,
                  measurementHeight=0.0, project=None):
        self.columns.append(Column.objects.create(
            name=name, positionInFile=positionInFile, columnType=columnType,
            valueType=valueType, instrumentCalibrationSlope=instrumentCalibrationSlope,
            instrumentCalibrationOffset=instrumentCalibrationOffset,
            dataLoggerCalibrationOffset=dataLoggerCalibrationOffset,
            dataLoggerCalibrationSlope=dataLoggerCalibrationSlope, measurementHeight=measurementHeight, project=project))

    def getColumn(self, columnName):
        return [c for c in self.columns if c.name == columnName][0]

    def addColumnSet(self,label,columnSet):
        self.columnSets[label] = columnSet

    def loadFromFile(self):
        cols = sorted([0]+[column.positionInFile for column in self.columns])
        df = pd.read_csv(self.fullyQualifiedPath(), sep=self.columnSeparator, skiprows=self.rowsToSkip, parse_dates=True, dayfirst=True, usecols=cols, index_col=0, na_values=self.badDataValues)
        df.columns = [name[0] for name in sorted([[column.name, column.positionInFile] for column in self.columns], key=lambda column: column[1])]
        self.data = df.apply(lambda x: pd.to_numeric(x), axis=0)
        #self.data = pd.to_numeric(df, errors='coerce')
        print("Data loaded: " + self.filename)

    def saveToFile(self):
        self.data.to_csv(self.fullyQualifiedPath(), sep=self.columnSeparator, float_format='%.4f')
        print("Data saved: " + self.filename)

    def clean(self):
        rowsBeforeClean = len(self.data)
        for badDataValue in self.badDataValues:
            try:
                self.data[self.data == badDataValue] = np.NaN
            except:
                pass
        self.data.dropna(inplace=True)
        rowsAfterClean = len(self.data)
        print(self.filename + ' - before clean: ' + str(rowsBeforeClean) + ' after clean: ' + str(rowsAfterClean) + ' (' + str(rowsBeforeClean-rowsAfterClean) + ' rows)')

    def applyInstrumentCalibrations(self, removeOriginalCalibration=False):
        for column in self.columns:
            if removeOriginalCalibration:
                self.data[column.name] = (self.data[column.name] - column.dataLoggerCalibrationOffset) / column.dataLoggerCalibrationSlope
            self.data[column.name] = self.data[column.name] * column.instrumentCalibrationSlope + column.instrumentCalibrationOffset
        for column in [c for c in self.columns if c.columnType == ColumnType.WIND_DIRECTION]:
            self.data[column.name] %= 360

    def saveAs(self, newFileName, containingDirectory):
        self.filename = newFileName
        self.directory = containingDirectory
        self.saveToFile()
        print("Datafile saved as: " + self.filename)

    def selectorFactory(self, columnName, operator, value):
        try:
            comparator = float(value)
        except:
            comparator = value

        if columnName == 'TIMESTAMP':
            return operator(self.data.index,comparator)
        elif isinstance(comparator,str):
            return operator(self.data[columnName],self.data[comparator])
        else:
            return operator(self.data[columnName],comparator)

    def addSelector(self, columnName=None, columnType=None, lowerLimit=None, upperLimit=None, valueType=None,
                    includeRange=True, rangeIncludesLowerBound=True, rangeIncludesUpperBound=True):

        self.selectors.append({'columnName': columnName, 'columnType': columnType,
                               'lowerLimit': lowerLimit, 'upperLimit': upperLimit,
                               'valueType': valueType, 'includeRange': includeRange,
                               'rangeIncludesLowerBound': rangeIncludesLowerBound,
                               'rangeIncludesUpperBound': rangeIncludesUpperBound})

    def selectData(self):
        selector = [True] * len(self.data)
        for s in self.selectors:
            message = 'Selecting '
            if s['columnName'] is not None:
                selectorColumns = (s['columnName'],)
                message += 'column ' + s['columnName']
            else:
                selectorColumns = (c.name for c in self.columns if c.columnType == s['columnType'] and c.valueType == s['valueType'])
                message += 'columns of type ' + str(s['columnType'])

            if s['includeRange']:
                upperOperator = op.le if s['rangeIncludesUpperBound'] else op.lt
                lowerOperator = op.ge if s['rangeIncludesLowerBound'] else op.gt
                mainOperator  = np.logical_and
                message += ' within range '
            else:
                lowerOperator = op.lt if s['rangeIncludesLowerBound'] else op.le
                upperOperator = op.gt if s['rangeIncludesUpperBound'] else op.ge
                mainOperator  = np.logical_or
                message += ' outside range '

            message += str(s['lowerLimit']) + ' - ' + str(s['upperLimit'])
            print(message)

            for column in selectorColumns:
                test1 = self.selectorFactory(column, lowerOperator, s['lowerLimit'])
                test2 = self.selectorFactory(column, upperOperator, s['upperLimit'])
                selector = np.logical_and(selector,
                                          mainOperator(self.selectorFactory(column, lowerOperator, s['lowerLimit']),
                                                       self.selectorFactory(column, upperOperator, s['upperLimit'])))

        self.data = self.data[selector]
        self.selectors = []


    def getMeasurementColumnSet(self, columnType):
        return {column.name: column.measurementHeight for column in self.columns if column.columnType == columnType and column.useInMultiHeightCalculations}

    def getColumnSet(self, columnSetName):
        return [c for c in self.columns if c.name in self.columnSets[columnSetName]]

    def addDerivedColumn(self, newColumn, functionToApply, columnArguments = (), kwargs = {}, measurementHeightValue=0.0, columnType=ColumnType.DERIVED, valueType=ValueType.DERIVED, project=None):
        # print('Adding ', newColumn, '... ', end=' ')
        print(columnArguments)
        if 'row' in signature(functionToApply).parameters:
            self.data[newColumn] = self.data.apply(functionToApply, axis=1, args=columnArguments, **kwargs)
        else:
            if columnArguments != ():
                args = [self.data[c] for c in columnArguments]
            else:
                args = []
            self.data[newColumn] = functionToApply(*args, **kwargs)

        self.addColumn(newColumn,len(self.columns)+1,columnType, valueType, measurementHeight=measurementHeightValue, project=project)
        #print("Done")

    def getHubHeightColumnName(self, turbine, columnType):
        for column in self.columns:
            if column.columnType == columnType and column.measurementHeight == turbine.hubHeight:
                return column.name
        print("Hub height column not found: " + columnType)
        return None

    def addRewsLevels(self, lidarColumns, turbine):
        previousMeasurementHeight = None
        for column in sorted(self.columns, key=lambda column: column.measurementHeight):
            if column in lidarColumns:
                if previousMeasurementHeight is None:
                    column.inferiorLimitHeight = turbine.lowerTipHeight()
                else:
                    column.inferiorLimitHeight = column.measurementHeight - (column.measurementHeight -  previousMeasurementHeight) / 2
                previousMeasurementHeight = column.measurementHeight
        previousMeasurementHeight = None
        for column in sorted(self.columns, reverse=True, key=lambda column: column.measurementHeight):
            if column in lidarColumns:
                if previousMeasurementHeight is None:
                    column.superiorLimitHeight = turbine.upperTipHeight()
                else:
                    column.superiorLimitHeight = column.measurementHeight + (previousMeasurementHeight - column.measurementHeight) / 2
                previousMeasurementHeight = column.measurementHeight

                column.segmentHeight = column.superiorLimitHeight - column.inferiorLimitHeight
                column.segmentArea = calc.stripeArea(turbine.radius(), column.inferiorLimitHeight-turbine.hubHeight, column.superiorLimitHeight-turbine.hubHeight)
                column.segmentWeighting = column.segmentArea / turbine.sweptArea()
