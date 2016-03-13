from __future__ import division
import pandas as pd
import numpy as np
import windAnalysis.calculation as calc
import configobj as cfg
import operator as op
from inspect import getargspec
from .ppaTypes import *


class Column(object):
    def __init__(self, name, positionInFile, columnType, valueType,
                 instrumentName=None, instrumentMake=None, instrumentModel=None,
                 instrumentCalibrationSlope=1.0, instrumentCalibrationOffset=0.0,
                 dataLoggerCalibrationSlope=1.0, dataLoggerCalibrationOffset=0.0,
                 measurementHeight=0.0):
        self.name = name
        self.positionInFile = positionInFile
        self.columnType = columnType
        self.valueType = valueType
        self.instrumentName = instrumentName
        self.instrumentMake = instrumentMake
        self.instrumentModel = instrumentModel
        self.instrumentCalibrationSlope = instrumentCalibrationSlope
        self.instrumentCalibrationOffset = instrumentCalibrationOffset
        self.dataLoggerCalibrationSlope = dataLoggerCalibrationSlope
        self.dataLoggerCalibrationOffset = dataLoggerCalibrationOffset
        self.measurementHeight = measurementHeight

        self.segmentWeighting = None
        self.inferiorLimitHeight = None
        self.superiorLimitHeight = None
        self.segmentHeight = None

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
        print("Datafile: " + self.filename)

    def fullyQualifiedPath(self):
        return self.directory + '/' + self.filename

    def configFile(self):
        return self.directory + '/' + self.filename.split('.')[0] + ".cfg"

    def addColumn(self, name, positionInFile, columnType, valueType,
                  instrumentName=None, instrumentMake=None, instrumentModel=None,
                  instrumentCalibrationSlope=1.0, instrumentCalibrationOffset=0.0,
                  dataLoggerCalibrationSlope=1.0, dataLoggerCalibrationOffset=0.0,
                  measurementHeight=0.0):
        self.columns.append(
            Column(name, positionInFile, columnType, valueType,
                   instrumentName, instrumentMake, instrumentModel,
                   instrumentCalibrationSlope, instrumentCalibrationOffset,
                   dataLoggerCalibrationSlope, dataLoggerCalibrationOffset,
                   measurementHeight))

    def getColumn(self, columnName):
        return [c for c in self.columns if c.name == columnName][0]

    def addColumnSet(self,label,columnSet):
        self.columnSets[label] = columnSet

    def loadFromFile(self):
        cols = sorted([0]+[column.positionInFile for column in self.columns])
        testvar = self.fullyQualifiedPath()
        df = pd.read_csv(self.fullyQualifiedPath(), sep=self.columnSeparator, skiprows=self.rowsToSkip, parse_dates=True, dayfirst=True, usecols=cols, index_col=0, na_values=self.badDataValues)
        df.columns = [name[0] for name in sorted([[column.name, column.positionInFile] for column in self.columns], key=lambda column: column[1])]
        self.data = pd.to_numeric(df, errors='coerce')
        print("Data loaded: " + self.filename)

    def saveToFile(self):
        self.data.to_csv(self.fullyQualifiedPath(), sep=self.columnSeparator, float_format='%.4f')
        print("Data saved: " + self.filename)

    def saveMetadata(self):
        config = cfg.ConfigObj()
        config['filename'] = self.filename
        config['directory'] = self.directory
        config['fileType'] = self.fileType
        config['columnSeparator'] = self.columnSeparator
        config['rowsToSkip'] = self.rowsToSkip
        config['badDataValues'] = self.badDataValues
        config['columns'] = {str(i): vars(column) for i, column in enumerate(self.columns)}
        config['columnSets'] = self.columnSets
        config['selectors'] = {str(i): selector for i, selector in enumerate(self.selectors)}
        config.filename = self.configFile()
        config.write()
        print("Metadata saved: " + self.filename)

    def loadMetadata(self):
        config = cfg.ConfigObj(self.configFile())
        self.filename = config['filename']
        self.directory = config['directory']
        self.fileType = FileType[config['fileType'].split('.')[1]]
        self.columnSeparator = config['columnSeparator']
        self.rowsToSkip = map(int, config['rowsToSkip'])
        self.badDataValues = config['badDataValues']
        for configColumn in sorted(config['columns'], key=int):
            self.columns.append(
                Column(config['columns'][configColumn]['name'],
                       int(config['columns'][configColumn]['positionInFile']),
                       ColumnType[config['columns'][configColumn]['columnType'].split('.')[1]],
                       ValueType[config['columns'][configColumn]['valueType'].split('.')[1]],
                       config['columns'][configColumn]['instrumentName'],
                       config['columns'][configColumn]['instrumentMake'],
                       config['columns'][configColumn]['instrumentModel'],
                       float(config['columns'][configColumn]['instrumentCalibrationSlope']),
                       float(config['columns'][configColumn]['instrumentCalibrationOffset']),
                       float(config['columns'][configColumn]['dataLoggerCalibrationSlope']),
                       float(config['columns'][configColumn]['dataLoggerCalibrationOffset']),
                       float(config['columns'][configColumn]['measurementHeight']))
            )
        for configColumnSet in config['columnSets']:
            self.columnSets[configColumnSet] = config['columnSets'][configColumnSet]
        for configSelector in sorted(config['selectors'], key=int):
            s = config['selectors'][configSelector]
            try:
                s['lowerLimit'] = float(s['lowerLimit'])
            except:
                pass
            try:
                s['upperLimit'] = float(s['upperLimit'])
            except:
                pass

            self.addSelector(columnName=None if s['columnName'] == 'None' else s['columnName'],
                             columnType=None if s['columnType'] == 'None' else ColumnType[s['columnType'].split('.')[1]],
                             lowerLimit=s['lowerLimit'],
                             upperLimit=s['upperLimit'],
                             valueType=None if s['valueType'] == 'None' else ValueType[s['valueType'].split('.')[1]],
                             includeRange=bool(s['includeRange']),
                             rangeIncludesLowerBound=bool(s['rangeIncludesLowerBound']),
                             rangeIncludesUpperBound=bool(s['rangeIncludesUpperBound']))
        print("Metadata loaded: " + self.filename)


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
        self.saveMetadata()
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

    def addDerivedColumn(self, newColumn, functionToApply, columnArguments = (), kwargs = {}, measurementHeightValue=0.0, columnType=ColumnType.DERIVED, valueType=ValueType.DERIVED):

        print('Adding ', newColumn, '... ', end=' ')
        if 'row' in getargspec(functionToApply).args:
            self.data[newColumn] = self.data.apply(functionToApply, axis=1, args=columnArguments, **kwargs)
        else:
            if columnArguments != ():
                args = [self.data[c] for c in columnArguments]
            else:
                args = []
            self.data[newColumn] = functionToApply(*args, **kwargs)

        self.addColumn(newColumn,len(self.columns)+1,columnType, valueType, measurementHeight=measurementHeightValue)
        print("Done")

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

