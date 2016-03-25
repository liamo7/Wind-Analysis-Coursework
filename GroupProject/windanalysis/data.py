from __future__ import division
import pandas as pd
import numpy as np
import windAnalysis.calculation as calc
import configobj as cfg
import operator as op
from inspect import getargspec
from .ppaTypes import *
from webinterface.models import Column

# class Column(object):
#     def __init__(self, name, positionInFile, columnType, valueType,
#                  instrumentName=None, instrumentMake=None, instrumentModel=None,
#                  instrumentCalibrationSlope=1.0, instrumentCalibrationOffset=0.0,
#                  dataLoggerCalibrationSlope=1.0, dataLoggerCalibrationOffset=0.0,
#                  measurementHeight=0.0):
#         self.name = name
#         self.positionInFile = positionInFile
#         self.columnType = columnType
#         self.valueType = valueType
#         self.instrumentName = instrumentName
#         self.instrumentMake = instrumentMake
#         self.instrumentModel = instrumentModel
#         self.instrumentCalibrationSlope = instrumentCalibrationSlope
#         self.instrumentCalibrationOffset = instrumentCalibrationOffset
#         self.dataLoggerCalibrationSlope = dataLoggerCalibrationSlope
#         self.dataLoggerCalibrationOffset = dataLoggerCalibrationOffset
#         self.measurementHeight = measurementHeight
#
#         self.segmentWeighting = None
#         self.inferiorLimitHeight = None
#         self.superiorLimitHeight = None
#         self.segmentHeight = None

