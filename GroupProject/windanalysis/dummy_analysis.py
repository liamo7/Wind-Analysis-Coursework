__author__ = 'brian'

import os as os
import matplotlib.pyplot as plt, mpld3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from .project import *
from .utility import *
from .turbine import *
from .ppaTypes import *
from django.http import HttpResponse


def dummy():
    project = Project('Dummy_project', os.getcwd())
    project.defineTurbine(Turbine('Nordex N90'))

    os.chdir(project.directory)

    windFile  = project.addDatafile('dummy_mast.txt', project.directory, FileType.METEO, columnSeparator='\t')
    powerFile = project.addDatafile('dummy_power.txt', project.directory, FileType.POWER, columnSeparator='\t')
    lidarFile = project.addDatafile('dummy_lidar.txt', project.directory, FileType.LIDAR, columnSeparator='\t')

    project.saveMetadata()
    print("Project setup complete")

    windFile.addColumn('Mast - 82m Wind Direction Mean',       1, ColumnType.WIND_DIRECTION,        ValueType.MEAN,               measurementHeight=82, instrumentCalibrationSlope=0.04581, instrumentCalibrationOffset=0.2638)
    windFile.addColumn('Mast - 80m Wind Speed Mean',       2, ColumnType.WIND_SPEED,        ValueType.MEAN,               measurementHeight=80, instrumentCalibrationSlope=0.04577, instrumentCalibrationOffset=0.2653)
    windFile.addColumn('Mast - 80m Wind Speed Std Dev',       3, ColumnType.WIND_SPEED,        ValueType.STANDARD_DEVIATION,               measurementHeight=80, instrumentCalibrationSlope=0.04577, instrumentCalibrationOffset=0.2688)
    windFile.addColumn('Mast - 64m Wind Speed Mean',       4, ColumnType.WIND_SPEED,        ValueType.MEAN,               measurementHeight=64, instrumentCalibrationSlope=0.04583, instrumentCalibrationOffset=0.2621)
    windFile.addColumn('Mast - 35.0m Wind Speed Mean',       5, ColumnType.WIND_SPEED,        ValueType.MEAN, measurementHeight=35, instrumentCalibrationSlope=0.04581, dataLoggerCalibrationSlope=0.0462)
    windFile.addColumn('Pressure (mBar)',       6, ColumnType.PRESSURE,          ValueType.MEAN,               measurementHeight=30)
    windFile.addColumn('Relative humidity (%)',               7, ColumnType.RELATIVE_HUMIDITY, ValueType.MEAN,               measurementHeight=30)
    windFile.addColumn('Temperature (C)',          8, ColumnType.TEMPERATURE,       ValueType.MEAN,               measurementHeight=30)
    windFile.addColumnSet('anemometers', ['Mast - 80m Wind Speed Mean','Mast - 64m Wind Speed Mean','Mast - 35.0m Wind Speed Mean'])
    windFile.saveMetadata()

    powerFile.addColumn('Power mean (kW)',            1,  ColumnType.POWER, ValueType.MEAN)
    powerFile.saveMetadata()

    lidarFile.addColumn("LiDAR - 132.5m Wind Speed Mean",       1,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=132.5)
    lidarFile.addColumn("LiDAR - 127.5m Wind Speed Mean",       2,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=127.5)
    lidarFile.addColumn("LiDAR - 117.5m Wind Speed Mean",       3,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=117.5)
    lidarFile.addColumn("LiDAR - 107.5m Wind Speed Mean",       4,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=107.5)
    lidarFile.addColumn("LiDAR - 97.5m Wind Speed Mean",       5,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=97.5)
    lidarFile.addColumn("LiDAR - 87.5m Wind Speed Mean",       6,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=87.5)
    lidarFile.addColumn("LiDAR - 77.5m Wind Speed Mean",       7,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=77.5)
    lidarFile.addColumn("LiDAR - 67.5m Wind Speed Mean",       8,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=67.5)
    lidarFile.addColumn("LiDAR - 57.5m Wind Speed Mean",       9,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=57.5)
    lidarFile.addColumn("LiDAR - 42.5m Wind Speed Mean",       10,ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=42.5)
    lidarFile.saveMetadata()

    windFile.loadFromFile()
    powerFile.loadFromFile()
    lidarFile.loadFromFile()

    windFile.clean()
    powerFile.clean()
    lidarFile.clean()

    combinedFile = synchroniseDataFiles('dummy_data.txt', project.directory, [windFile, powerFile, lidarFile])
    combinedFile.saveMetadata()
    combinedFile.saveToFile()

    print("File setup complete")

    siteCalibrationFactors = {190: {'slope': 1.0152, 'offset': 0},
                              200: {'slope': 1.0135, 'offset': 0},
                              210: {'slope': 0.9957, 'offset': 0},
                              220: {'slope': 1.0094, 'offset': 0},
                              230: {'slope': 1.0211, 'offset': 0},
                              240: {'slope': 1.0063, 'offset': 0}}

    combinedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)

    combinedFile.addDerivedColumn('airDensity', calculation.airDensity, columnArguments=('Pressure (mBar)', 'Temperature (C)', 'Relative humidity (%)'), columnType=ColumnType.AIR_DENSITY)
    combinedFile.addDerivedColumn('turbulenceIntensity', calculation.turbulenceIntensity, columnArguments=('Mast - 80m Wind Speed Mean', 'Mast - 80m Wind Speed Std Dev'),columnType = ColumnType.TURBULENCE_INTENSITY)
    combinedFile.addDerivedColumn('windShearExponentPolyfit', calculation.windShearExponentPolyfit, kwargs= {'columnSet': combinedFile.getColumnSet('anemometers')},columnType=ColumnType.WIND_SHEAR_EXPONENT)
    combinedFile.addDerivedColumn('twoHeightWindShearExponent', calculation.windShearExponentTwoHeights, columnArguments=("Mast - 64m Wind Speed Mean", "Mast - 80m Wind Speed Mean"), kwargs= {'lowerHeight': 64, 'upperHeight': 80}, columnType=ColumnType.WIND_SHEAR_EXPONENT)
    combinedFile.addDerivedColumn('wind_direction_bin', calculation.bin, columnArguments=('Mast - 82m Wind Direction Mean',), kwargs={'binWidth': 10})
    combinedFile.addDerivedColumn('siteCorrectedWindSpeed', calculation.siteCorrectedWindSpeed, columnArguments=('Mast - 80m Wind Speed Mean', 'wind_direction_bin'), kwargs={'factors': siteCalibrationFactors})
    combinedFile.addDerivedColumn('normalisedWindSpeed', calculation.normalisedWindSpeed, columnArguments=('siteCorrectedWindSpeed', 'airDensity'), columnType=ColumnType.WIND_SPEED)
    combinedFile.addDerivedColumn('windSpeedBin', calculation.bin, columnArguments=('normalisedWindSpeed',), kwargs={'binWidth': 0.5, 'zeroIsBinStart': False})
    combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction', calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve}))
    combinedFile.addDerivedColumn('powerDeviation', calculation.powerDeviation, columnArguments=('Power mean (kW)', 'normalisedWindSpeed'), kwargs={'powerCurve': project.turbine.warrantedPowerCurve})


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

