# from django.db import models
# from .utils import *
# import json
#
# class ProjectManager(models.Manager):
#     def getUploadPath(self, filename):
#         return '{0}\sitecalibration\{1}'.format(self.title, filename)
#
#
#
# # class Turbine(models.Model):
# #     name = models.CharField(max_length=128, blank=False)
# #
# #     manufacturer = models.CharField(max_length=200, blank=False)
# #     model = models.CharField(max_length=120, blank=False)
# #     diameter = models.DecimalField(decimal_places=2, max_digits=10)
# #     hub_height = models.DecimalField(decimal_places=2, max_digits=10)
# #
# #     bins = models.CharField(max_length=300)
# #     powerInKillowats = models.CharField(max_length=300)
# #
# #     oneMeterStrip = models.BooleanField(default=False)
# #
# #     # A turbine can be linked with many projects though
# #
# #     def __str__(self):
# #         return self.name
# #
# #     def setBins(self, data):
# #         self.bins = json.dumps(data)
# #
# #     def getBins(self):
# #         return json.loads(self.bins)
# #
# #     def setPowerInKillowats(self, data):
# #         self.powerInKillowats = json.dumps(data)
# #
# #     def getPowerInKillowats(self):
# #         return json.loads(self.powerInKillowats)
# #
# #     def createPowerCurveDict(self):
# #         powerCurveDict = {
# #             'bin': self.getBins(),
# #             'powerInKilowatts': self.getPowerInKillowats()
# #         }
# #
# #         return powerCurveDict
# #
# #     def stripes(self):
# #         self.stripes = None
#
# from django.db import models
# import json
# import numpy as np
# import test_wind.calculation as calc
# from math import modf, pi, log10, acos
# from pandas import DataFrame, concat, Series
# from test_wind.ppaTypes import *
#
#
# class Turbine(models.Model):
#     name = models.CharField(max_length=128, blank=False)
#
#     manufacturer = models.CharField(max_length=200, blank=False)
#     model = models.CharField(max_length=120, blank=False)
#     diameter = models.DecimalField(decimal_places=2, max_digits=10)
#     hub_height = models.DecimalField(decimal_places=2, max_digits=10)
#
#     bins = models.CharField(max_length=300)
#     powerInKillowats = models.CharField(max_length=300)
#
#     oneMeterStrip = models.BooleanField(default=False)
#
#
#     def __str__(self):
#         return self.name
#
#     def setBins(self, data):
#         self.bins = json.dumps(data)
#
#     def getBins(self):
#         return json.loads(self.bins)
#
#     def setPowerInKillowats(self, data):
#         self.powerInKillowats = json.dumps(data)
#
#     def getPowerInKillowats(self):
#         return json.loads(self.powerInKillowats)
#
#     def createPowerCurveDict(self):
#         # self.powerCurveDict = {
#         #     'bin': self.getBins(),
#         #     'powerInKilowatts': self.getPowerInKillowats()
#         # }
#
#         self.powerCurveDict = {'bin':[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5],
#                               'powerInKilowatts':[0,0,0,0,0,0,0,29,76,136,207,292,390,504,635,787,958,1147,1352,1570,1799,2036,2231,2368,2454,2496,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,0]}
#
#         return self.powerCurveDict
#
#     def getWarrantedPowerCurve(self):
#         return PowerCurve(self.createPowerCurveDict(), interpolate=True)
#
#     def radius(self):
#         return self.diameter / 2
#
#     def lowerTipHeight(self):
#         return self.hub_height - self.radius()
#
#     def upperTipHeight(self):
#         return self.hub_height + self.radius()
#
#     def sweptArea(self):
#         return pi*pow(self.diameter/2,2)
#
#     def addOneMetreHorizontalStripes(self):
#         previousHeight = self.lowerTipHeight()
#         self.stripes = []
#         diameterFraction = np.round(self.diameter % 1,7)
#         loopLimit = self.diameter
#         if diameterFraction > 0:
#             loopLimit = self.diameter - 1
#             height = round(previousHeight + diameterFraction/2,7)
#             upperLimit = height - self.hub_height
#             lowerLimit = previousHeight - self.hub_height
#             stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
#             proportion = stripeArea / self.sweptArea()
#             windSpeedHeight = round(previousHeight + diameterFraction/4,7)
#             self.stripes.append({'stripeArea': stripeArea,
#                                  'proportion': proportion,
#                                  'windSpeedHeight': windSpeedHeight})
#             previousHeight = height
#         for i in np.arange(loopLimit):
#             height = round(previousHeight + 1,7)
#             upperLimit = height - self.hub_height
#             lowerLimit = previousHeight - self.hub_height
#             stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
#             proportion = stripeArea / self.sweptArea()
#             windSpeedHeight = round(previousHeight + 0.5, 7)
#             self.stripes.append({'stripeArea': stripeArea,
#                                  'proportion': proportion,
#                                  'windSpeedHeight': windSpeedHeight})
#             previousHeight = height
#         if diameterFraction > 0:
#             height = round(previousHeight + diameterFraction/2,7)
#             upperLimit = height - self.hub_height
#             lowerLimit = previousHeight - self.hub_height
#             stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
#             proportion = stripeArea / self.sweptArea()
#             windSpeedHeight = round(previousHeight + diameterFraction/4,7)
#             self.stripes.append({'stripeArea': stripeArea,
#                                  'proportion': proportion,
#                                  'windSpeedHeight': windSpeedHeight})
#
#
# class PowerCurve(object):
#     def __init__(self, pcdict, cutin=4, cutout=25, referenceAirDensity=1.225, interpolate = False):
#         """ Dict elements: {bin, powerInKilowatts, meanWindSpeed, recordsPerBin, binStatus}
#         """
#         self.data = DataFrame(pcdict)
#         self.cutin = cutin
#         self.cutout = cutout
#         self.referenceAirDensity = referenceAirDensity
#         if interpolate:
#             self.data_1 = self.interpolate(interpolationStep=0.1)
#             self.data_01 = self.interpolate(interpolationStep=0.01)
#             self.data_001 = self.interpolate(interpolationStep=0.001)
#
#     # def cutin(self, interpolationStep=11.0):
#     #     if interpolationStep == 11.0:
#     #         return self.data[self.data['powerInKilowatts']>0]['bin'].min()
#     #     else:
#     #         return self.data[self.data['powerInKilowatts']>0]['bin'].min() - interpolationStep
#     #
#     # def cutout(self):
#     #     return self.data[self.data['powerInKilowatts']>0]['bin'].max() + self.windSpeedStep()
#
#     def calculatePowerCoefficients(self, rotorRadius):
#         try:
#             self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / calc.availablePowerInWind(self.data['meanWindSpeed'], self.referenceAirDensity, rotorRadius)
#         except:
#             self.data['powerCoefficient'] = self.data['powerInKilowatts'] * 1000 / calc.availablePowerInWind(self.data.index, self.referenceAirDensity, rotorRadius)
#
#     def windSpeedStep(self):
#         return self.data.ix[1, 'bin'] - self.data.ix[0, 'bin']
#
#     def getPower(self,windSpeed, decimalPlaces=0):
#         if windSpeed > self.cutout:
#             return 0
#
#         scalingFactor = np.power(10,decimalPlaces)
#         indexForWindSpeed = int(round(windSpeed * scalingFactor))
#         if decimalPlaces == 0:
#             dataframe = self.data
#         elif decimalPlaces == 1:
#             dataframe = self.data_1
#         elif decimalPlaces == 2:
#             dataframe = self.data_01
#         elif decimalPlaces == 3:
#             dataframe = self.data_001
#         else:
#             raise
#
#         return round(dataframe['powerInKilowatts'].iloc[indexForWindSpeed], decimalPlaces)
#
#     def calculateAep(self, annualMeanWindSpeed):
#         self.data['aepMeasured'] = 0.0
#         firstMeasuredBin = self.data[self.data['binStatus'] != BinStatus.EXCLUDED].index.min()
#
#         for row in np.arange(firstMeasuredBin, len(self.data.index)):
#             if self.data.iloc[row]['binStatus'] != BinStatus.EXCLUDED:
#                 try:
#                     rayleigh_prev = rayleigh
#                     power_prev = power
#                 except:
#                     rayleigh_prev = calc.rayleigh(self.data.ix[0, 'meanWindSpeed'] - 0.5, annualMeanWindSpeed)
#                     power_prev = 0.
#
#                 rayleigh = calc.rayleigh(self.data.iloc[row]['meanWindSpeed'], annualMeanWindSpeed)
#                 power = self.data.iloc[row]['powerInKilowatts']
#
#                 self.data.ix[self.data.index[row], 'aepMeasured'] = 8760 * (rayleigh - rayleigh_prev) * (power + power_prev) / 2
#
#                 # feedback = {'annualMeanWindSpeed}': annualMeanWindSpeed,
#                 #             'windSpeed': self.data.iloc[row]['meanWindSpeed'],
#                 #             'power': power,
#                 #             'rayleigh': rayleigh,
#                 #             'previousPower': power_prev,
#                 #             'rayleighPrev': rayleigh_prev,
#                 #             'aep': 8760 * (rayleigh - rayleigh_prev) * (power + power_prev) / 2}
#                 # # print(feedback)
#
#         lastMeasuredBin = self.data[self.data['binStatus'] != BinStatus.EXCLUDED].index.max()
#         totalNumberOfBins = self.cutout / self.windSpeedStep() + 1
#         numberOfRowsToAdd = totalNumberOfBins - self.data.index[-1]
#
#         if numberOfRowsToAdd > 0:
#             padding = DataFrame({'bin': np.arange(self.data.ix[lastMeasuredBin, 'bin'] + self.windSpeedStep(),
#                                                   self.cutout + self.windSpeedStep(),
#                                                   self.windSpeedStep())})
#             # print(self.data)
#             # print(padding)
#             # print(totalNumberOfBins)
#             # print(len(self.data.index))
#             # print(np.arange(len(self.data.index), totalNumberOfBins + 1))
#             padding.index = [x for x in np.arange(len(self.data.index), totalNumberOfBins + 1)]
#             # print(padding)
#
#             # padding = DataFrame({'bin': self.data.iloc[-numberOfRowsToAdd:]['bin'].as_matrix()},
#             #                     index=np.arange(self.data.index[-11]+11, self.cutout/self.windSpeedStep()))
#             # padding['bin'] += numberOfRowsToAdd * self.windSpeedStep()
#             self.data = concat([self.data, padding])
#         self.data['aepExtrapolated'] = self.data['aepMeasured']
#         # maxPower = self.data[self.data['binStatus'] != BinStatus.EXCLUDED]['powerInKilowatts'].max()
#         rayleigh_prev = calc.rayleigh(self.data.ix[lastMeasuredBin, 'bin'], annualMeanWindSpeed)
#         for row in np.arange(lastMeasuredBin + 1, len(self.data.index)):
#             rayleigh = calc.rayleigh(self.data.iloc[row]['bin'], annualMeanWindSpeed)
#             self.data.ix[self.data.index[row], 'aepExtrapolated'] = 8760 * (rayleigh - rayleigh_prev) * self.data.iloc[lastMeasuredBin]['powerInKilowatts']
#             # print('Padding row '+str(row),)
#             # print('   rayleigh: '+str(rayleigh),)
#             # print('   rayleigh_prev: '+str(rayleigh_prev),)
#             # print('   power: '+str(self.data.iloc[lastMeasuredBin]['powerInKilowatts']))
#             rayleigh_prev = rayleigh
#
#
#     def aepMeasured(self):
#         try:
#             return self.data['aepMeasured'].sum()
#         except:
#             # print('Calculate AEP first!')
#             return 0.0
#
#     def aepExtrapolated(self):
#         try:
#             return self.data['aepExtrapolated'].sum()
#         except:
#             # print('Calculate AEP first!')
#             return 0.0
#
#     def statistics(self):
#         if 'powerCoefficient' in self.data:
#             # print(self.data[['bin',
#                              'meanWindSpeed',
#                              'recordsPerBin',
#                              'powerInKilowatts',
#                              'binStatus',
#                              'powerCoefficient',
#                              'aepMeasured',
#                              'aepExtrapolated']])
#         else:
#             # print(self.data[['bin',
#                              'meanWindSpeed',
#                              'recordsPerBin',
#                              'powerInKilowatts',
#                              'binStatus']])
#
#     def interpolate(self, interpolationStep=1.0):
#         newLength = int((self.data.index[-1]-self.data.index[0])/interpolationStep+1)
#         scalingFactor = int(1/interpolationStep)
#         newDataFrame = DataFrame(index=np.linspace(self.data.index[0],self.data.index[-1],newLength))
#         extendedDataFrame = concat([self.data,newDataFrame], axis=1)
#         extendedDataFrame.set_index(np.arange(newLength))
#         # extendedDataFrame['powerInKilowatts'].iloc[int(round((self.cutout()-interpolationStep)*scalingFactor))] = \
#         #     extendedDataFrame['powerInKilowatts'].iloc[int(round((self.cutout()-self.windSpeedStep())*scalingFactor))].tolist()
#         extendedDataFrame['powerInKilowatts'].iloc[int(round(self.cutout * scalingFactor))] = \
#             extendedDataFrame['powerInKilowatts'].iloc[int(round(self.cutout * scalingFactor))].tolist()
#         return extendedDataFrame.interpolate().set_index(np.arange(newLength))
#
#     def line(self, axes, style='r-'):
#         try:
#             axes.plot(self.data['meanWindSpeed'], self.data['powerInKilowatts'], style)
#         except:
#             axes.plot(self.data['bin'], self.data['powerInKilowatts'], style)
#
#
#
#
# class Project(models.Model):
#
#     title = models.CharField(max_length=64, unique=True, blank=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#
#     site_calibration_allowed = models.BooleanField(default=False)
#     site_calibration_file = models.FileField(upload_to=ProjectManager.getUploadPath)
#
#     turbine = models.ForeignKey(Turbine, on_delete=models.CASCADE)
#
#     # @property
#     # def dataFilePaths(self):
#     #     return # printAllFilesInDirectory()
#
#     class Meta:
#         verbose_name = 'Project'
#         verbose_name_plural = 'Projects'
#
#     def __str__(self):
#         return self.title
#
#
# class Analysis(models.Model):
#     title = models.CharField(max_length=64, blank=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Analysis'
#         verbose_name_plural = 'Analyses'
#
#     def __str__(self):
#         return self.title
#
#
#
#
