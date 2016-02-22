import configobj as cfg
from .calculation import *
import pandas as pd
from .data import Datafile
from .turbine import *
from .ppaTypes import *


class Project(object):
    def __init__(self, name=None, directory=None):
        self.name = name
        self.directory = directory
        self.datafiles = []
        self.turbine = None
        self.siteCalibrationFactors = {}
        print("Project: " + self.name)

    def defineTurbine(self, turbine):
        self.turbine = turbine
        print("Turbine: " + self.turbine.name)

    def addDatafile(self, name=None, fileType=None, rowsToSkip=[], columnSeparator='\t', badDataValues=[]):
        self.datafiles.append(name)
        return Datafile(name, fileType, rowsToSkip, columnSeparator, badDataValues)

    def stringifySiteCalibrationFactors(self):
        siteCalibrationFactorsAsStrings = {}
        for scf, value in self.siteCalibrationFactors.iteritems():
            slope = str(value['slope'])
            offset = str(value['offset'])
            siteCalibrationFactorsAsStrings.update({str(scf): {'slope': slope, 'offset': offset}})
        return siteCalibrationFactorsAsStrings

    def deStringifySiteCalibrationFactors(self, factorDict):
        siteCalibrationFactorsDict = {}
        for scf, value in factorDict.iteritems():
            slope = float(value['slope'])
            offset = float(value['offset'])
            siteCalibrationFactorsDict.update({int(scf): {'slope': slope, 'offset': offset}})
        return siteCalibrationFactorsDict


    def saveMetadata(self):
        config = cfg.ConfigObj()
        config['name'] = self.name
        config['directory'] = self.directory
        config['turbine'] = '' if self.turbine is None else self.turbine.name
        config['datafiles'] = self.datafiles
        config['siteCalibrationFactors'] = self.stringifySiteCalibrationFactors()

        config.filename = self.directory + '/' + self.name + '.cfg'
        config.write()
        print("Project metadata saved")

    def configFile(self):
        return self.directory + '/' + self.name + ".cfg"

    def loadMetadata(self):
        config = cfg.ConfigObj(self.configFile())
        self.name = config['name']
        self.directory = config['directory']
        self.turbine = Turbine(config['turbine'])
        self.datafiles = config['datafiles']
        self.siteCalibrationFactors = self.deStringifySiteCalibrationFactors(config['siteCalibrationFactors'])
        print("Loaded project metadata: " + self.name)

    def makeMeasuredPowerCurve(self, data, windSpeedColumn, powerColumn, binColumn, binWidth=0.5):
        data['recordsPerBin'] = 1
        grouped = data.groupby(binColumn).aggregate({windSpeedColumn: 'mean',
                                                    powerColumn: 'mean',
                                                    'recordsPerBin': 'size'})
        completeDataframe = pd.DataFrame(index=np.arange(grouped.index[0],
                                         grouped.index[len(grouped.index)-1]+binWidth,
                                         binWidth))
        completeDataframe = pd.concat([grouped, completeDataframe], axis=1).fillna(0)
        completeDataframe.columns = ['recordsPerBin', 'powerInKilowatts', 'meanWindSpeed']
        completeDataframe['bin'] = completeDataframe.index
        completeDataframe['binStatus'] = BinStatus.EXCLUDED

        invalidBins = 0
        for thisBin in completeDataframe.index:
            if invalidBins >= 2:
                break
            if completeDataframe.ix[thisBin, 'recordsPerBin'] < 3:
                try:
                    completeDataframe.ix[thisBin, 'powerInKilowatts'] = \
                        calc.interpolate(completeDataframe.ix[thisBin - 1, 'powerInKilowatts'], \
                                         completeDataframe.ix[thisBin + 1, 'powerInKilowatts'])
                    invalidBins += 1
                    completeDataframe.ix[thisBin, 'binStatus'] = BinStatus.INTERPOLATED
                except:
                    pass
            else:
                completeDataframe.ix[thisBin, 'binStatus'] = BinStatus.MEASURED

        firstMeasuredBin = completeDataframe[completeDataframe['binStatus'] == BinStatus.MEASURED].index.min()
        firstPaddedBin = completeDataframe[completeDataframe['binStatus'] == BinStatus.MEASURED].index.max() + 1
        completeDataframe[firstPaddedBin:len(completeDataframe.index)]['binStatus'] = BinStatus.EXCLUDED

        frontPaddingBins = np.arange(0,completeDataframe.loc[firstMeasuredBin]['bin'] - binWidth, binWidth)
        frontPadding = pd.DataFrame({'bin': [x for x in frontPaddingBins],
                                     'recordsPerBin': [0 for x in frontPaddingBins],
                                     'powerInKilowatts': [0 for x in frontPaddingBins],
                                     'meanWindSpeed': [0 for x in frontPaddingBins],
                                     'binStatus': BinStatus.EXCLUDED})
        completeDataframe = pd.concat([frontPadding, completeDataframe])

        # pcdict = completeDataframe.to_dict(orient='list')
        # # pcdict['bin'] = completeDataframe.index
        #
        # thisRow = 0
        # while thisRow < len(pcdict['bin']) and invalidBins < 2:
        #     if pcdict['recordsPerBin'][thisRow] < 3:
        #         try:
        #             previousPower = pcdict['powerInKilowatts'][thisRow-11]
        #             nextPower = pcdict['powerInKilowatts'][thisRow+11]
        #             pcdict['powerInKilowatts'][thisRow] = (previousPower + nextPower) / 2
        #             invalidBins += 11
        #             pcdict['binStatus'][thisRow] = BinStatus.INTERPOLATED
        #         except:
        #             break
        #     else:
        #         pcdict['binStatus'][thisRow] = BinStatus.MEASURED
        #     thisRow += 11

        # thisRow -= 11
        # while pcdict['binStatus'][thisRow] == BinStatus.EXCLUDED or pcdict['binStatus'][thisRow] == BinStatus.INTERPOLATED:
        #     pcdict['binStatus'][thisRow] = BinStatus.EXCLUDED
        #     thisRow -= 11
        #
        # thisRow = 0
        #
        # while pcdict['binStatus'][thisRow] == BinStatus.EXCLUDED or pcdict['binStatus'][thisRow] == BinStatus.INTERPOLATED:
        #     pcdict['binStatus'][thisRow] = BinStatus.EXCLUDED
        #     thisRow += 11

        return PowerCurve(completeDataframe.to_dict(orient='list'),
                          cutin=self.turbine.warrantedPowerCurve.cutin,
                          cutout=self.turbine.warrantedPowerCurve.cutout)
