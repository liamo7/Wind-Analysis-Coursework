__author__ = 'brian'

import os as os
import matplotlib.pyplot as plt, mpld3
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from .utility import *
from webinterface.models import Turbine, Project
from .ppaTypes import *


def dummy(project, fileList):

    print("HERTE")

    windFile = None
    powerFile = None
    lidarFile = None

    if 'windDataFile' in fileList:
        windFile = fileList['windDataFile']

    if 'powerDataFile' in fileList:
        powerFile = fileList['powerDataFile']

    if 'lidarDataFile' in fileList:
        lidarFile = fileList['lidarDataFile']

    if windFile is None and powerFile is None and lidarFile is None:
        return

    files = []



    if windFile:
        windFile.addColumn('Mast - 82m Wind Direction Mean',       1, ColumnType.WIND_DIRECTION,        ValueType.MEAN,               measurementHeight=82, instrumentCalibrationSlope=0.04581, instrumentCalibrationOffset=0.2638, project=project)
        windFile.addColumn('Mast - 80m Wind Speed Mean',       2, ColumnType.WIND_SPEED,        ValueType.MEAN,               measurementHeight=80, instrumentCalibrationSlope=0.04577, instrumentCalibrationOffset=0.2653, project=project)
        windFile.addColumn('Mast - 80m Wind Speed Std Dev',       3, ColumnType.WIND_SPEED,        ValueType.STANDARD_DEVIATION,               measurementHeight=80, instrumentCalibrationSlope=0.04577, instrumentCalibrationOffset=0.2688, project=project)
        windFile.addColumn('Mast - 64m Wind Speed Mean',       4, ColumnType.WIND_SPEED,        ValueType.MEAN,               measurementHeight=64, instrumentCalibrationSlope=0.04583, instrumentCalibrationOffset=0.2621, project=project)
        windFile.addColumn('Mast - 35.0m Wind Speed Mean',       5, ColumnType.WIND_SPEED,        ValueType.MEAN, measurementHeight=35, instrumentCalibrationSlope=0.04581, dataLoggerCalibrationSlope=0.0462, project=project)
        windFile.addColumn('Pressure (mBar)',       6, ColumnType.PRESSURE,          ValueType.MEAN,               measurementHeight=30, project=project)
        windFile.addColumn('Relative humidity (%)',               7, ColumnType.RELATIVE_HUMIDITY, ValueType.MEAN,               measurementHeight=30, project=project)
        windFile.addColumn('Temperature (C)',          8, ColumnType.TEMPERATURE,       ValueType.MEAN,               measurementHeight=30, project=project)
        windFile.addColumnSet('anemometers', ['Mast - 80m Wind Speed Mean','Mast - 64m Wind Speed Mean','Mast - 35.0m Wind Speed Mean'])
        windFile.loadFromFile()
        windFile.clean()
        files.append(windFile)

    if powerFile:
        powerFile.addColumn('Power mean (kW)', 1,  ColumnType.POWER, ValueType.MEAN, project=project)
        powerFile.loadFromFile()
        powerFile.clean()
        files.append(powerFile)

    if lidarFile:
        lidarFile.addColumn("LiDAR - 132.5m Wind Speed Mean",       1,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=132.5, project=project)
        lidarFile.addColumn("LiDAR - 127.5m Wind Speed Mean",       2,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=127.5, project=project)
        lidarFile.addColumn("LiDAR - 117.5m Wind Speed Mean",       3,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=117.5, project=project)
        lidarFile.addColumn("LiDAR - 107.5m Wind Speed Mean",       4,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=107.5, project=project)
        lidarFile.addColumn("LiDAR - 97.5m Wind Speed Mean",       5,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=97.5, project=project)
        lidarFile.addColumn("LiDAR - 87.5m Wind Speed Mean",       6,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=87.5, project=project)
        lidarFile.addColumn("LiDAR - 77.5m Wind Speed Mean",       7,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=77.5, project=project)
        lidarFile.addColumn("LiDAR - 67.5m Wind Speed Mean",       8,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=67.5, project=project)
        lidarFile.addColumn("LiDAR - 57.5m Wind Speed Mean",       9,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=57.5, project=project)
        lidarFile.addColumn("LiDAR - 42.5m Wind Speed Mean",       10,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=42.5, project=project)
        lidarFile.loadFromFile()
        lidarFile.clean()
        files.append(lidarFile)


    combinedFile = synchroniseDataFiles('dummy_data.txt', project.directory, files)
    combinedFile.saveToFile()

    print("File setup complete")

    siteCalibrationFactors = {190: {'slope': 1.0152, 'offset': 0},
                              200: {'slope': 1.0135, 'offset': 0},
                              210: {'slope': 0.9957, 'offset': 0},
                              220: {'slope': 1.0094, 'offset': 0},
                              230: {'slope': 1.0211, 'offset': 0},
                              240: {'slope': 1.0063, 'offset': 0}}

    combinedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)

    combinedFile.addDerivedColumn('airDensity',           calculation.airDensity, columnArguments=('Pressure (mBar)', 'Temperature (C)', 'Relative humidity (%)'), columnType=ColumnType.AIR_DENSITY, project=project)
    combinedFile.addDerivedColumn('turbulenceIntensity',                  calculation.turbulenceIntensity, columnArguments=('Mast - 80m Wind Speed Mean', 'Mast - 80m Wind Speed Std Dev'),columnType = ColumnType.TURBULENCE_INTENSITY, project=project)
    combinedFile.addDerivedColumn('windShearExponentPolyfit',            calculation.windShearExponentPolyfit, kwargs= {'columnSet': combinedFile.getColumnSet('anemometers')},columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)
    combinedFile.addDerivedColumn('twoHeightWindShearExponent',             calculation.windShearExponentTwoHeights, columnArguments=("Mast - 64m Wind Speed Mean", "Mast - 80m Wind Speed Mean"), kwargs= {'lowerHeight': 64, 'upperHeight': 80}, columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)
    combinedFile.addDerivedColumn('wind_direction_bin',                     calculation.bin, columnArguments=('Mast - 82m Wind Direction Mean',), kwargs={'binWidth': 10}, project=project)
    combinedFile.addDerivedColumn('siteCorrectedWindSpeed',                    calculation.siteCorrectedWindSpeed, columnArguments=('Mast - 80m Wind Speed Mean', 'wind_direction_bin'), kwargs={'factors': siteCalibrationFactors}, project=project)
    combinedFile.addDerivedColumn('normalisedWindSpeed',                    calculation.normalisedWindSpeed, columnArguments=('siteCorrectedWindSpeed', 'airDensity'), columnType=ColumnType.WIND_SPEED, project=project)
    combinedFile.addDerivedColumn('windSpeedBin',                           calculation.bin, columnArguments=('normalisedWindSpeed',), kwargs={'binWidth': 0.5, 'zeroIsBinStart': False}, project=project)
    combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction',      calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve()}), project=project)
    combinedFile.addDerivedColumn('powerDeviation',                         calculation.powerDeviation, columnArguments=('Power mean (kW)', 'normalisedWindSpeed'), kwargs={'powerCurve': project.turbine.warrantedPowerCurve()}, project=project)


    combinedFile.selectData()
    combinedFile.saveAs('dummy_derived.txt', project.directory)


    print("Derived file created")

    datafile = combinedFile

    measuredPowerCurve = project.makeMeasuredPowerCurve(datafile.data,'normalisedWindSpeed','Power mean (kW)','windSpeedBin')
    measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())

    meanWindSpeed = 7.5

    measuredPowerCurve.aepAdded(meanWindSpeed)
    measuredPowerCurve.statistics()
    print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))

    fg, ax = plt.subplots()
    plt.title('Power curve scatter')
    plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)

    mpld3.save_html(fg, 'templates/project/test.html')


# mock dict for columns

def normaliseColData(data):
    col = {'header': 'Mast - 82m Wind Direction Mean', 'colType': 'WIND_DIRECTION', 'valType': 'MEAN',
           'measurementHeight': 82, 'instrumentCalibrationSlope': 0.04581, 'instrumentCalibrationOffset': 0.2638,
           'dataLoggerCalibrationSlope': 0.0462, 'dataLoggerCalibrationOffset': 0.04321};






