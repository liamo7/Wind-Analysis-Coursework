__author__ = 'brian'

import matplotlib.pyplot as plt, mpld3
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from windAnalysis.ppaTypes import *
from .models import JsonDataFile, Analysis
import json
from .utils import PythonObjectEncoder, as_python_object
from GroupProject.settings import MEDIA_ROOT, STATIC_DIR

def processAnalysis(project, files, calc, analysis):


    derivedFile = files[-1]
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

    derivedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)


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
        derivedFile.addDerivedColumn(newColumn=calc['row' + index]['calcType'], functionToApply=eval('calculation.' + calc['row' + index]['calcType']), columnArguments=calc['row' + index]['cols'], columnType=ColumnType(calc['row' + index]['colType'] + 1), kwargs=kwargs, project=project)

    derivedFile.selectData()
    derivedFile.saveAs('derived.txt', project.getDerivedFilePath() + '/' + analysis.title + '/')

    jsonDataFile, created = JsonDataFile.objects.get_or_create(name='derived', analysisID=analysis.id)
    jsonDataFile.jsonData = json.dumps(derivedFile, cls=PythonObjectEncoder)
    jsonDataFile.save()
    analysis.derivedDataFile = jsonDataFile
    analysis.save()

    print("Derived file created")
    # -------PostProcessing stage analysis---------------------#
    datafile = derivedFile

    # measuredPowerCurve = project.makeMeasuredPowerCurve(datafile.data,'normalisedWindSpeed','Power mean (kW)','windSpeedBin')
    # measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())
    #
    # meanWindSpeed = 7.5
    #
    # measuredPowerCurve.aepAdded(meanWindSpeed)
    # #measuredPowerCurve.statistics()
    # #print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    # #print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))






def postAnalysis(project):

    t = Analysis.objects.get(title='Analysis2')

    dataFileObj = JsonDataFile.objects.get(name='derived', analysisID=t.id)
    data = json.loads(dataFileObj.jsonData, object_hook=as_python_object)

    plt.switch_backend('agg')
    fg, ax = plt.subplots()

    plt.title('Power curve scatter')
    # plotting.powerCurve(datafile.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)

    plotting.powerCurve(data.data, 'normalisedWindSpeed', 'Power mean (kW)', ax)
    mpld3.save_html(fg, 'templates/project/test.html')
    print(STATIC_DIR)
    plt.savefig(STATIC_DIR + '/test.png')