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
                kwargDict['powerCurve'] = eval('project.turbine.' + calc['row' + index]['kwargs']['powerCurve'] + '()')

            if key == 'factors':
                kwargDict['factors'] = siteCalibrationFactors

        if 'powerCurve' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['powerCurve']

        if 'factors' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['factors']

        kwargs = {**calc['row'+index]['kwargs'], **kwargDict}
        combinedFile.addDerivedColumn(newColumn=calc['row' + index]['calcType'], functionToApply=eval('calculation.' + calc['row' + index]['calcType']), columnArguments=calc['row' + index]['cols'], columnType=ColumnType(calc['row' + index]['colType'] + 1), kwargs=kwargs, project=project)

    combinedFile.selectData()
    combinedFile.saveAs('derived.txt', project.getDerivedFilePath())


    print("Derived file created")
    # -------PostProcessing stage analysis---------------------#
    datafile = combinedFile

    print("HERE")
    measuredPowerCurve = project.makeMeasuredPowerCurve(datafile.data,'normalisedWindSpeed','Power mean (kW)','windSpeedBin')
    measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())
    print("FA")
    meanWindSpeed = 7.5

    measuredPowerCurve.aepAdded(meanWindSpeed)
    measuredPowerCurve.statistics()
    print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))

    plt.switch_backend('agg')
    fg, ax = plt.subplots()

    plt.title('Power curve scatter')
    # plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)

    plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)
    mpld3.save_html(fg, 'templates/project/test.html')




