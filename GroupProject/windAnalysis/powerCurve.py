import numpy as np
from pandas import DataFrame, concat
import windAnalysis.calculation as calc
from .ppaTypes import *
from math import log10

__author__ = 'Brian'


class PowerCurve(object):
    def __init__(self, pcdict, cutin=4, cutout=25, windSpeedStep=1.0, referenceAirDensity=1.225, interpolate=False, warranted=False):
        """ Dict elements: {bin, powerInKilowatts, meanWindSpeed, recordsPerBin, binStatus}
        """
        self.data = DataFrame(pcdict)
        if warranted:
            self.data['binStatus'] = BinStatus.WARRANTED
            self.data['meanWindSpeed'] = self.data['bin']
        self.cutin = cutin
        self.cutout = cutout
        self.windSpeedStep = windSpeedStep
        self.referenceAirDensity = referenceAirDensity
        if interpolate:
            self.data_1 = self.interpolate(interpolationStep=0.1)
            self.data_01 = self.interpolate(interpolationStep=0.01)
            self.data_001 = self.interpolate(interpolationStep=0.001)

    def isWarranted(self):
        if BinStatus.WARRANTED in self.data['binStatus'].tolist():
            return True
        return False

    def calculatePowerCoefficients(self, rotorRadius):
        try:
            self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / calc.availablePowerInWind(
                self.data['meanWindSpeed'], self.referenceAirDensity, rotorRadius)
        except:
            self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / calc.availablePowerInWind(
                self.data.index, self.referenceAirDensity, rotorRadius)

    def getBinIndex(self, windSpeed):
        print(self.data['bin'].index.values)
        return self.data[self.data['bin'] == windSpeed].index.values[0]

    def padded(self, truncateAtCutout=True):
        firstWindSpeed = self.data.loc[self.data['binStatus'] != BinStatus.EXCLUDED, 'bin'].min()
        lastWindSpeed = self.data.loc[self.data['binStatus'] != BinStatus.EXCLUDED, 'bin'].max()

        if not truncateAtCutout and self.getBinIndex(lastWindSpeed) > self.cutout:
            maxBin = int(lastWindSpeed / self.windSpeedStep + 1)
        else:
            maxBin = int(self.cutout / self.windSpeedStep + 1)

        newPowerCurve = self
        newPowerCurve.data = self.data[self.getBinIndex(firstWindSpeed):self.getBinIndex(lastWindSpeed) + 1]
        newPowerCurve.data.index = self.data['bin'] / self.windSpeedStep

        ix = list(range(maxBin))
        newPowerCurve.data = newPowerCurve.data.reindex(ix, newPowerCurve.data.columns, method='pad', fill_value=0)
        firstBin = newPowerCurve.getBinIndex(firstWindSpeed)
        lastBin = newPowerCurve.getBinIndex(lastWindSpeed)

        if firstBin > 0:
            newPowerCurve.data.loc[0:firstBin - 1, 'bin'] = newPowerCurve.data.loc[0:firstBin - 1].index.values * newPowerCurve.windSpeedStep
            newPowerCurve.data.loc[0:firstBin - 1, 'meanWindSpeed'] = newPowerCurve.data.loc[0:firstBin - 1, 'bin']
            newPowerCurve.data.loc[0:firstBin - 1, 'binStatus'] = BinStatus.PADDED

        if lastBin < maxBin:
            newPowerCurve.data.loc[lastBin + 1:maxBin, 'bin'] = newPowerCurve.data[lastBin + 1:maxBin].index.values * newPowerCurve.windSpeedStep
            newPowerCurve.data.loc[lastBin + 1:maxBin, 'meanWindSpeed'] = newPowerCurve.data.loc[lastBin + 1:maxBin, 'bin']
            newPowerCurve.data.loc[lastBin + 1:maxBin, 'binStatus'] = BinStatus.PADDED
            newPowerCurve.data.loc[lastBin + 1:maxBin, 'recordsPerBin'] = 0

        return newPowerCurve

    def getPower(self, windSpeed, decimalPlaces=0):
        if windSpeed > self.cutout:
            return 0

        scalingFactor = np.power(10, decimalPlaces)
        indexForWindSpeed = int(round(windSpeed * scalingFactor))
        try:
            if decimalPlaces == 0:
                dataFrame = self.data
            elif decimalPlaces == 1:
                dataFrame = self.data_1
            elif decimalPlaces == 2:
                dataFrame = self.data_01
            elif decimalPlaces == 3:
                dataFrame = self.data_001
            else:
                raise Exception()
        except:
            print('This number of decimal places is not supported')

        return round(dataFrame['powerInKilowatts'].iloc[indexForWindSpeed], decimalPlaces)

    def validated(self):
        newPC = self

        interpolatedBins = 0
        for thisBin in newPC.data.index:
            if interpolatedBins >= 2:
                break
            if newPC.data.loc[thisBin, 'recordsPerBin'] < 3:
                try:
                    if newPC.data.loc[thisBin-1, 'binStatus'] == BinStatus.MEASURED and \
                                    newPC.data.loc[thisBin+1, 'recordsPerBin'] >= 3:
                        newPC.data.loc[thisBin, 'powerInKilowatts'] = \
                            calc.interpolate(newPC.data.loc[thisBin - 1, 'powerInKilowatts'],
                                             newPC.data.loc[thisBin + 1, 'powerInKilowatts'])
                        interpolatedBins += 1
                        newPC.data.loc[thisBin, 'binStatus'] = BinStatus.INTERPOLATED
                except:
                    pass
            else:
                newPC.data.loc[thisBin, 'binStatus'] = BinStatus.MEASURED

        return newPC

    def aepAdded(self, annualMeanWindSpeed):
        newPowerCurve = self
        newPowerCurve.data['aep_' + str(annualMeanWindSpeed)] = 0.0
        if newPowerCurve.isWarranted():
            firstBin = newPowerCurve.data[newPowerCurve.data['binStatus'] == BinStatus.WARRANTED].index.min()
        else:
            firstBin = newPowerCurve.data[newPowerCurve.data['binStatus'] == BinStatus.MEASURED].index.min()

        rayleigh_prev = calc.rayleigh(newPowerCurve.data.loc[firstBin, 'meanWindSpeed'] - 0.5, annualMeanWindSpeed)
        power_prev = 0.

        for row in range(firstBin, len(newPowerCurve.data.index)):
            rayleigh = calc.rayleigh(newPowerCurve.data.loc[row, 'meanWindSpeed'], annualMeanWindSpeed)
            aep = 8760 * (rayleigh - rayleigh_prev) * (newPowerCurve.data.loc[row, 'powerInKilowatts'] + power_prev) / 2
            newPowerCurve.data.loc[newPowerCurve.data.index[row], 'aep_' + str(annualMeanWindSpeed)] = aep
            rayleigh_prev = rayleigh
            power_prev = newPowerCurve.data.loc[row, 'powerInKilowatts']

        return newPowerCurve

    def aepMeasured(self, annualWindSpeed):
        try:
            firstBin = self.data[self.data['binStatus'] != BinStatus.PADDED].index.min()
            lastBin = self.data[self.data['binStatus'] != BinStatus.PADDED].index.max()
            return self.data.loc[firstBin:lastBin, 'aep_'+str(annualWindSpeed)].sum()
        except:
            print('Calculate AEP first!')
            return 0.0

    def aepExtrapolated(self, annualWindSpeed):
        try:
            firstBin = self.data[self.data['binStatus'] != BinStatus.PADDED].index.min()
            return self.data.loc[firstBin:len(self.data), 'aep_'+str(annualWindSpeed)].sum()
        except:
            print('Calculate AEP first!')
            return 0.0

    def statistics(self):
        if 'powerCoefficient' in self.data:
            print(self.data)
        else:
            print(self.data[['bin',
                             'meanWindSpeed',
                             'recordsPerBin',
                             'powerInKilowatts',
                             'binStatus']])

    def interpolate(self, interpolationStep=1.0):
        ix = np.arange(0, self.data['bin'].max() + interpolationStep, interpolationStep)
        extendedDataFrame = self.data.reindex(ix).interpolate()
        extendedDataFrame.index = list(range(len(extendedDataFrame)))
        extendedDataFrame['bin'] = extendedDataFrame['bin']
        extendedDataFrame['binStatus'].fillna(BinStatus.INTERPOLATED)
        return extendedDataFrame

    def line(self, axes, style='r-'):
        try:
            axes.plot(self.data['meanWindSpeed'], self.data['powerInKilowatts'], style)
        except:
            axes.plot(self.data['bin'], self.data['powerInKilowatts'], style)
