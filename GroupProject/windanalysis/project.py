import configobj as cfg
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

    def addDatafile(self, name=None, containingDirectory=None, fileType=None, rowsToSkip=[], columnSeparator='\t', badDataValues=[]):
        self.datafiles.append(name)
        return Datafile(name, containingDirectory, fileType, rowsToSkip, columnSeparator, badDataValues)

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

    def makeMeasuredPowerCurve(self, data, windSpeedColumn, powerColumn, binColumn, binWidth=0.5, airDensity=1.225):
        grouped = data.groupby(binColumn).aggregate({windSpeedColumn: 'mean',
                                                    powerColumn: 'mean',
                                                    binColumn: 'count'})
        grouped = grouped.rename(columns={binColumn: 'recordsPerBin', windSpeedColumn: 'meanWindSpeed', powerColumn: 'powerInKilowatts'})
        grouped['bin'] = grouped.index
        grouped['binStatus'] = BinStatus.EXCLUDED
        grouped.index = list(range(len(grouped)))

        powerCurve = PowerCurve(grouped.to_dict(orient='list'),
                                cutin=self.turbine.warrantedPowerCurve.cutin,
                                cutout=self.turbine.warrantedPowerCurve.cutout,
                                windSpeedStep=binWidth,
                                referenceAirDensity=airDensity)

        return powerCurve.validated().padded()
