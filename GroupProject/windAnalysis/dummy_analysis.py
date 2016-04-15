__author__ = 'brian'

import matplotlib.pyplot as plt, mpld3
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from .ppaTypes import *


def dummy(project, files, calc):


    combinedFile = files[-1]
    # For an analysis, a file will be selected on which to perform the analysis on
    # this could be combined file, raw data files ?
    #

    #-------Processing stage analysis---------------------#
    siteCalibrationFactors = {190: {'slope': 1.0152, 'offset': 0},
                              200: {'slope': 1.0135, 'offset': 0},
                              210: {'slope': 0.9957, 'offset': 0},
                              220: {'slope': 1.0094, 'offset': 0},
                              230: {'slope': 1.0211, 'offset': 0},
                              240: {'slope': 1.0063, 'offset': 0}}
    # combinedFile.addDerivedColumn('windShearExponentPolyfit',            calculation.windShearExponentPolyfit, kwargs= {'columnSet': combinedFile.getColumnSet('anemometers')},columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)

    combinedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)

    # for row in calc:
    #     kwargDict = {}
    #
    #     for key, value in calc[row]['kwargs'].items():
    #
    #         if key == 'powerCurve':
    #             kwargDict['powerCurve'] = eval('project.turbine.' + calc[row]['kwargs']['powerCurve'] + '()')
    #             del calc[row]['kwargs']['powerCurve']
    #             break
    #
    #         if key == 'factors':
    #             kwargDict['factors'] = siteCalibrationFactors
    #             del calc[row]['kwargs']['factors']
    #             break
    #
    #     kwargs = {**calc[row]['kwargs'], **kwargDict}
    #    # print(kwargs)
    #     combinedFile.addDerivedColumn(newColumn=calc[row]['calcType'], functionToApply=eval('calculation.' + calc[row]['calcType']), columnArguments=calc[row]['cols'], columnType=ColumnType(calc[row]['colType'] + 1), kwargs=kwargs, project=project)


    for count, row in enumerate(calc):
        kwargDict = {}
        count += 1
        index = str(count)
        for key, value in calc['row' + str(index)]['kwargs'].items():
            if key == 'powerCurve':
                print("POWERCURVE")
                kwargDict['powerCurve'] = eval('project.turbine.' + calc['row' + index]['kwargs']['powerCurve'] + '()')

            if key == 'factors':
                kwargDict['factors'] = siteCalibrationFactors

        if 'powerCurve' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['powerCurve']

        if 'factors' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['factors']

        kwargs = {**calc['row'+index]['kwargs'], **kwargDict}
        print(kwargs)
        print(str(calc['row' + index]['calcType']) + ' ' + str(calc['row' + index]['cols']) + ' ' + str(kwargs))
        # if count == 8:
        #     combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction',      calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve()}), project=project)
        # elif count == 9:
        #     combinedFile.addDerivedColumn('powerDeviation', calculation.powerDeviation,
        #                                     columnArguments=('Power mean (kW)', 'normalisedWindSpeed'),
        #                                     kwargs={'powerCurve': project.turbine.warrantedPowerCurve()}, project=project)
        # else:
        combinedFile.addDerivedColumn(newColumn=calc['row' + index]['calcType'], functionToApply=eval('calculation.' + calc['row' + index]['calcType']), columnArguments=calc['row' + index]['cols'], columnType=ColumnType(calc['row' + index]['colType'] + 1), kwargs=kwargs, project=project)


    #combinedFile.addDerivedColumn(calc[row]['calcType'], eval('calculation.' + calc[row]['calcType']), columnArguments=calc[row]['cols'], columnType=ColumnType(calc[row]['colType'] + 1), kwargs=calc[row]['kwargs'], project=project)

    # combinedFile.addDerivedColumn(calc['row1']['calcType'], eval('calculation.' + calc['row1']['calcType']), columnArguments=calc['row1']['cols'], columnType=ColumnType(calc['row1']['colType'] + 1), project=project)
    # combinedFile.addDerivedColumn(calc['row2']['calcType'], eval('calculation.' + calc['row2']['calcType']), columnArguments=calc['row2']['cols'], columnType=ColumnType(calc['row2']['colType'] + 1), project=project)
    # combinedFile.addDerivedColumn(calc['row3']['calcType'], eval('calculation.' + calc['row3']['calcType']), columnArguments=calc['row3']['cols'], columnType=ColumnType(calc['row3']['colType'] + 1), kwargs=calc['row3']['kwargs'], project=project)
    # combinedFile.addDerivedColumn(calc['row4']['calcType'], eval('calculation.' + calc['row4']['calcType']), columnArguments=calc['row4']['cols'], columnType=ColumnType(calc['row4']['colType'] + 1), kwargs=calc['row4']['kwargs'], project=project)
    # combinedFile.addDerivedColumn(calc['row5']['calcType'], eval('calculation.' + calc['row5']['calcType']), columnArguments=calc['row5']['cols'], columnType=ColumnType(calc['row5']['colType'] + 1), kwargs=calc['row5']['kwargs'], project=project)
    # combinedFile.addDerivedColumn(calc['row6']['calcType'], eval('calculation.' + calc['row6']['calcType']), columnArguments=calc['row6']['cols'], columnType=ColumnType(calc['row6']['colType'] + 1), kwargs=calc['row6']['kwargs'], project=project)
    # combinedFile.addDerivedColumn(calc['row7']['calcType'], eval('calculation.' + calc['row7']['calcType']), columnArguments=calc['row7']['cols'], columnType=ColumnType(calc['row7']['colType'] + 1), kwargs=calc['row7']['kwargs'], project=project)
    # combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction',      calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve()}), project=project)
    # combinedFile.addDerivedColumn(calc['row9']['calcType'], eval('calculation.' + calc['row9']['calcType']), columnArguments=calc['row9']['cols'], columnType=ColumnType(calc['row9']['colType'] + 1), kwargs=calc['row9']['kwargs'], project=project)

    # combinedFile.addDerivedColumn('airDensity', calculation.airDensity, columnArguments=('Pressure (mBar)', 'Temperature (C)', 'Relative humidity (%)'), columnType=ColumnType.AIR_DENSITY, project=project)
    # combinedFile.addDerivedColumn('turbulenceIntensity',                  calculation.turbulenceIntensity, columnArguments=('Mast - 80m Wind Speed Mean', 'Mast - 80m Wind Speed Std Dev'),columnType = ColumnType.TURBULENCE_INTENSITY, project=project)
    # combinedFile.addDerivedColumn('twoHeightWindShearExponent',             calculation.twoHeightWindShearExponent, columnArguments=("Mast - 64m Wind Speed Mean", "Mast - 80m Wind Speed Mean"), kwargs= {'lowerHeight': 64, 'upperHeight': 80}, columnType=ColumnType.WIND_SHEAR_EXPONENT, project=project)
    # combinedFile.addDerivedColumn('wind_direction_bin',                     calculation.bin, columnArguments=('Mast - 82m Wind Direction Mean',), kwargs={'binWidth': 10}, project=project)
    # combinedFile.addDerivedColumn('siteCorrectedWindSpeed',                    calculation.siteCorrectedWindSpeed, columnArguments=('Mast - 80m Wind Speed Mean', 'wind_direction_bin'), kwargs={'factors': siteCalibrationFactors}, project=project)
    # combinedFile.addDerivedColumn('normalisedWindSpeed',                    calculation.normalisedWindSpeed, columnArguments=('siteCorrectedWindSpeed', 'airDensity'), columnType=ColumnType.WIND_SPEED, project=project)
    # combinedFile.addDerivedColumn('windSpeedBin',                           calculation.bin, columnArguments=('normalisedWindSpeed',), kwargs={'binWidth': 0.5, 'zeroIsBinStart': False}, project=project)
    # combinedFile.addDerivedColumn('hubHeightSpecificEnergyProduction',      calculation.specificEnergyProduction, kwargs=({'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': project.turbine.warrantedPowerCurve()}), project=project)
    # combinedFile.addDerivedColumn('powerDeviation', calculation.powerDeviation,
    #                                    columnArguments=('Power mean (kW)', 'normalisedWindSpeed'),
    #                                    kwargs={'powerCurve': project.turbine.warrantedPowerCurve()}, project=project)

    combinedFile.selectData()
    combinedFile.saveAs('dummy_derived.txt', project.directory)


    print("Derived file created")
    # -------PostProcessing stage analysis---------------------#
    datafile = combinedFile

    # measuredPowerCurve = project.makeMeasuredPowerCurve(datafile.data,'normalisedWindSpeed','Power mean (kW)','windSpeedBin')
    # measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())
    #
    # meanWindSpeed = 7.5
    #
    # measuredPowerCurve.aepAdded(meanWindSpeed)
    # #measuredPowerCurve.statistics()
    # #print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    # #print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))
    #
    # plt.switch_backend('agg')
    # fg, ax = plt.subplots()
    #
    # plt.title('Power curve scatter')
    # plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)
    #
    # mpld3.save_html(fg, 'templates/project/test.html')




