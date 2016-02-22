__author__ = 'Brian'
import numpy as np
from .calculation import *
from math import modf, pi, log10, acos
from pandas import DataFrame, concat, Series
from .ppaTypes import *


class Turbine(object):
    def __init__(self, turbine='Undefined'):
        self.name = turbine
        self.stripes = None
        if turbine == 'Enercon_E70':
            self.manufacturer = 'Enercon'
            self.model = 'E-70'
            self.diameter = 71.0
            self.hubHeight = 64.0
            powerCurveDict = {'bin': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
                              'powerInKilowatts': [0,0,2,18,56,127,240,400,626,892,1223.0,1590.0,1900.0,2080.0,2230.0,2300.0,2310.0,2310.0,2310.0,2310.0,2310.0,2310.0,2310.0,2310.0,2310.0,2310.0,0.]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, cutin=2, interpolate=True)
            self.addOneMetreHorizontalStripes()
        elif turbine == 'Siemens SWT-2.3-101':
            self.manufacturer = 'Siemens'
            self.model = 'SWT-2.3-101'
            self.diameter = 100.6
            self.hubHeight = 73.5
            powerCurveDict = {'bin':[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
                              'powerInKilowatts':[0,0,0,0,113,234,431,708,1076,1545,2015,2241,2294,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,0]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, interpolate=True)
            self.addOneMetreHorizontalStripes()
        elif turbine == 'Nordex N90':
            self.manufacturer = 'Nordex'
            self.model = 'N90'
            self.diameter = 90
            self.hubHeight = 80
            powerCurveDict = {'bin':[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5],
                              'powerInKilowatts':[0,0,0,0,0,0,0,29,76,136,207,292,390,504,635,787,958,1147,1352,1570,1799,2036,2231,2368,2454,2496,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,0]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, interpolate=True)
            self.addOneMetreHorizontalStripes()
        else:
            self.warrantedPowerCurve = None
            self.manufacturer = None
            self.model = None
            self.diameter = None
            self.hubHeight = None
            self.stripes = []

    def radius(self):
        return self.diameter / 2

    def lowerTipHeight(self):
        return self.hubHeight - self.radius()

    def upperTipHeight(self):
        return self.hubHeight + self.radius()

    def sweptArea(self):
        return pi*pow(self.diameter/2,2)


    def addOneMetreHorizontalStripes(self):
        previousHeight = self.lowerTipHeight()
        self.stripes = []
        diameterFraction = np.round(self.diameter % 1,7)
        loopLimit = self.diameter

        if diameterFraction > 0:
            loopLimit = self.diameter - 1
            height = round(previousHeight + diameterFraction/2,7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight

            stripeArea = stripeAream(self.radius(), lowerLimit, upperLimit)

            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction/4,7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})
            previousHeight = height

        for i in np.arange(loopLimit):
            height = round(previousHeight + 1,7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = stripeAream(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + 0.5, 7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})
            previousHeight = height
        if diameterFraction > 0:
            height = round(previousHeight + diameterFraction/2,7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = stripeAream(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction/4,7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})


class PowerCurve(object):
    def __init__(self, pcdict, cutin=4, cutout=25, referenceAirDensity=1.225, interpolate = False):
        """ Dict elements: {bin, powerInKilowatts, meanWindSpeed, recordsPerBin, binStatus}
        """
        self.data = DataFrame(pcdict)
        self.cutin = cutin
        self.cutout = cutout
        self.referenceAirDensity = referenceAirDensity
        if interpolate:
            self.data_1 = self.interpolate(interpolationStep=0.1)
            self.data_01 = self.interpolate(interpolationStep=0.01)
            self.data_001 = self.interpolate(interpolationStep=0.001)

    # def cutin(self, interpolationStep=11.0):
    #     if interpolationStep == 11.0:
    #         return self.data[self.data['powerInKilowatts']>0]['bin'].min()
    #     else:
    #         return self.data[self.data['powerInKilowatts']>0]['bin'].min() - interpolationStep
    #
    # def cutout(self):
    #     return self.data[self.data['powerInKilowatts']>0]['bin'].max() + self.windSpeedStep()

    def calculatePowerCoefficients(self, rotorRadius):
        try:
            self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / availablePowerInWind(self.data['meanWindSpeed'], self.referenceAirDensity, rotorRadius)
        except:
            self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / availablePowerInWind(self.data.index, self.referenceAirDensity, rotorRadius)

    def windSpeedStep(self):
        return self.data.ix[1, 'bin'] - self.data.ix[0, 'bin']

    def getPower(self,windSpeed, decimalPlaces=0):
        if windSpeed > self.cutout:
            return 0

        scalingFactor = np.power(10,decimalPlaces)
        indexForWindSpeed = int(round(windSpeed * scalingFactor))
        if decimalPlaces == 0:
            dataframe = self.data
        elif decimalPlaces == 1:
            dataframe = self.data_1
        elif decimalPlaces == 2:
            dataframe = self.data_01
        elif decimalPlaces == 3:
            dataframe = self.data_001
        else:
            raise

        return round(dataframe['powerInKilowatts'].iloc[indexForWindSpeed], decimalPlaces)

    def calculateAep(self, annualMeanWindSpeed):
        self.data['aepMeasured'] = 0.0
        firstMeasuredBin = self.data[self.data['binStatus'] != BinStatus.EXCLUDED].index.min()

        for row in np.arange(firstMeasuredBin, len(self.data.index)):
            if self.data.iloc[row]['binStatus'] != BinStatus.EXCLUDED:
                try:
                    rayleigh_prev = rayleigh
                    power_prev = power
                except:
                    rayleigh_prev = rayleigh(self.data.ix[0, 'meanWindSpeed'] - 0.5, annualMeanWindSpeed)
                    power_prev = 0.

                rayleigh = rayleigh(self.data.iloc[row]['meanWindSpeed'], annualMeanWindSpeed)
                power = self.data.iloc[row]['powerInKilowatts']

                self.data.ix[self.data.index[row], 'aepMeasured'] = 8760 * (rayleigh - rayleigh_prev) * (power + power_prev) / 2

                # feedback = {'annualMeanWindSpeed}': annualMeanWindSpeed,
                #             'windSpeed': self.data.iloc[row]['meanWindSpeed'],
                #             'power': power,
                #             'rayleigh': rayleigh,
                #             'previousPower': power_prev,
                #             'rayleighPrev': rayleigh_prev,
                #             'aep': 8760 * (rayleigh - rayleigh_prev) * (power + power_prev) / 2}
                # print(feedback)

        lastMeasuredBin = self.data[self.data['binStatus'] != BinStatus.EXCLUDED].index.max()
        totalNumberOfBins = self.cutout / self.windSpeedStep() + 1
        numberOfRowsToAdd = totalNumberOfBins - self.data.index[-1]

        if numberOfRowsToAdd > 0:
            padding = DataFrame({'bin': np.arange(self.data.ix[lastMeasuredBin, 'bin'] + self.windSpeedStep(),
                                                  self.cutout + self.windSpeedStep(),
                                                  self.windSpeedStep())})
            print(self.data)
            print(padding)
            print(totalNumberOfBins)
            print(len(self.data.index))
            print(np.arange(len(self.data.index), totalNumberOfBins + 1))
            padding.index = [x for x in np.arange(len(self.data.index), totalNumberOfBins + 1)]
            print(padding)

            # padding = DataFrame({'bin': self.data.iloc[-numberOfRowsToAdd:]['bin'].as_matrix()},
            #                     index=np.arange(self.data.index[-11]+11, self.cutout/self.windSpeedStep()))
            # padding['bin'] += numberOfRowsToAdd * self.windSpeedStep()
            self.data = concat([self.data, padding])
        self.data['aepExtrapolated'] = self.data['aepMeasured']
        # maxPower = self.data[self.data['binStatus'] != BinStatus.EXCLUDED]['powerInKilowatts'].max()
        rayleigh_prev = rayleigh(self.data.ix[lastMeasuredBin, 'bin'], annualMeanWindSpeed)
        for row in np.arange(lastMeasuredBin + 1, len(self.data.index)):
            rayleigh = rayleigh(self.data.iloc[row]['bin'], annualMeanWindSpeed)
            self.data.ix[self.data.index[row], 'aepExtrapolated'] = 8760 * (rayleigh - rayleigh_prev) * self.data.iloc[lastMeasuredBin]['powerInKilowatts']
            print('Padding row '+str(row),)
            print('   rayleigh: '+str(rayleigh),)
            print('   rayleigh_prev: '+str(rayleigh_prev),)
            print('   power: '+str(self.data.iloc[lastMeasuredBin]['powerInKilowatts']))
            rayleigh_prev = rayleigh


    def aepMeasured(self):
        try:
            return self.data['aepMeasured'].sum()
        except:
            print('Calculate AEP first!')
            return 0.0

    def aepExtrapolated(self):
        try:
            return self.data['aepExtrapolated'].sum()
        except:
            print('Calculate AEP first!')
            return 0.0

    def statistics(self):
        if 'powerCoefficient' in self.data:
            print(self.data[['bin',
                             'meanWindSpeed',
                             'recordsPerBin',
                             'powerInKilowatts',
                             'binStatus',
                             'powerCoefficient',
                             'aepMeasured',
                             'aepExtrapolated']])
        else:
            print(self.data[['bin',
                             'meanWindSpeed',
                             'recordsPerBin',
                             'powerInKilowatts',
                             'binStatus']])

    def interpolate(self, interpolationStep=1.0):
        newLength = int((self.data.index[-1]-self.data.index[0])/interpolationStep+1)
        scalingFactor = int(1/interpolationStep)
        newDataFrame = DataFrame(index=np.linspace(self.data.index[0],self.data.index[-1],newLength))
        extendedDataFrame = concat([self.data,newDataFrame], axis=1)
        extendedDataFrame.set_index(np.arange(newLength))
        # extendedDataFrame['powerInKilowatts'].iloc[int(round((self.cutout()-interpolationStep)*scalingFactor))] = \
        #     extendedDataFrame['powerInKilowatts'].iloc[int(round((self.cutout()-self.windSpeedStep())*scalingFactor))].tolist()
        extendedDataFrame['powerInKilowatts'].iloc[int(round(self.cutout * scalingFactor))] = \
            extendedDataFrame['powerInKilowatts'].iloc[int(round(self.cutout * scalingFactor))].tolist()
        return extendedDataFrame.interpolate().set_index(np.arange(newLength))

    def line(self, axes, style='r-'):
        try:
            axes.plot(self.data['meanWindSpeed'], self.data['powerInKilowatts'], style)
        except:
            axes.plot(self.data['bin'], self.data['powerInKilowatts'], style)


