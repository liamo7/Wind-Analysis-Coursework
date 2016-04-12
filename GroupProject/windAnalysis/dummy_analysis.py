__author__ = 'brian'

import matplotlib.pyplot as plt, mpld3
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from .ppaTypes import *


def dummy(project, files):


    combinedFile = files[-1]
    # For an analysis, a file will be selected on which to perform the analysis on
    # this could be combined file, raw data files ?
    #

    siteCalibrationFactors = {190: {'slope': 1.0152, 'offset': 0},
                              200: {'slope': 1.0135, 'offset': 0},
                              210: {'slope': 0.9957, 'offset': 0},
                              220: {'slope': 1.0094, 'offset': 0},
                              230: {'slope': 1.0211, 'offset': 0},
                              240: {'slope': 1.0063, 'offset': 0}}

    combinedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)

    combinedFile.addDerivedColumn('airDensity', calculation.airDensity, columnArguments=('Pressure (mBar)', 'Temperature (C) ', 'Relative humidity (%)'), columnType=ColumnType.AIR_DENSITY, project=project)
    combinedFile.addDerivedColumn('turbulenceIntensity',                  calculation.turbulenceIntensity, columnArguments=('Mast - 80m Wind Speed Mean', 'Mast - 80m Wind Speed Std Dev'),columnType = ColumnType.TURBULENCE_INTENSITY, project=project)
    #combinedFile.addDerivedColumn('windShearExponentPolyfit',            calculation.windShearExponentPolyfit, kwargs= {'columnSet': combinedFile.getColumnSet('anemometers')},columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)
    combinedFile.addDerivedColumn('twoHeightWindShearExponent',             calculation.windShearExponentTwoHeights, columnArguments=("Mast - 64m Wind Speed Mean", "Mast - 80m Wind Speed Mean"), kwargs= {'lowerHeight': 64, 'upperHeight': 80}, columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)
    combinedFile.addDerivedColumn('wind_direction_bin',                     calculation.bin, columnArguments=('Mast - 82m Wind Direction Mean',), kwargs={'binWidth': 10}, project=project)
    combinedFile.addDerivedColumn('siteCorrectedWindSpeed',                    calculation.siteCorrectedWindSpeed, columnArguments=('Mast - 80m Wind Speed Mean', 'wind_direction_bin'), kwargs={'factors': siteCalibrationFactors}, project=project)
    combinedFile.addDerivedColumn('normalisedWindSpeed',                    calculation.normalisedWindSpeed, columnArguments=('siteCorrectedWindSpeed', 'airDensity'), columnType=ColumnType.WIND_SPEED, project=project)
    combinedFile.addDerivedColumn('windSpeedBin',                           calculation.bin, columnArguments=('normalisedWindSpeed',), kwargs={'binWidth': 0.5, 'zeroIsBinStart': False}, project=project)
    combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction',      calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve()}), project=project)
    combinedFile.addDerivedColumn('powerDeviation', calculation.powerDeviation,
                                       columnArguments=('Power mean (kW) ', 'normalisedWindSpeed'),
                                       kwargs={'powerCurve': project.turbine.warrantedPowerCurve()}, project=project)

    combinedFile.selectData()
    combinedFile.saveAs('dummy_derived.txt', project.directory)


    print("Derived file created")

    datafile = combinedFile

    measuredPowerCurve = project.makeMeasuredPowerCurve(datafile.data,'normalisedWindSpeed','Power mean (kW) ','windSpeedBin')
    measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())

    meanWindSpeed = 7.5

    measuredPowerCurve.aepAdded(meanWindSpeed)
    measuredPowerCurve.statistics()
    print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))

    fg, ax = plt.subplots()
    plt.title('Power curve scatter')
    plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW) ', ax)

    mpld3.save_html(fg, 'templates/project/test.html')








