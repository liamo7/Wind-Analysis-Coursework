from unittest import TestCase
from .powerCurve import *
from math import pi, exp
from .ppaTypes import *
import numpy as np

__author__ = 'Brian'


class TestPowerCurve(TestCase):
    def setUp(self):
        self.powerCurveDict = {
            'bin': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
            'powerInKilowatts': [0, 0, 2, 18, 56, 127, 240, 400, 626, 892, 1223.00, 1590.00, 1900.00, 2080.00, 2230.00, 2300.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00]}
        self.pcWarranted = PowerCurve(self.powerCurveDict, cutin=2, interpolate=True, warranted=True)

        """ MeasuredDict has a gap a the start, a gap at the end, three excluded bins at the end of the measured range
            and one invalid bin at 15 m/s which needs to be interpolated
        """
        self.measuredDict = {
            'bin': [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5],
            'meanWindSpeed': [0, 0, 0, 0, 2.567573133, 3.049436362, 3.533027362, 3.983400558, 4.474223476, 5.009557067, 5.504098461, 5.998415614, 6.498971865, 7.015330066, 7.480049959, 7.997179138, 8.502244019, 8.998963008, 9.475691685, 9.990098489, 10.50277807, 10.98143994, 11.46608957, 11.99179217, 12.5162771, 13.0617489, 13.50124321, 13.96582903, 14.4596459, 15.21054198, 15.64749192, 16.19555048, 16.51495769, 0, 17.4731942],
            'powerInKilowatts': [0, 0, 0, 0, 38.92428571, 52.11617073, 86.35728814, 120.0694681, 187.5647619, 267.643125, 359.7845161, 471.5351648, 611.4993056, 767.7156028, 935.707971, 1183.769231, 1400.960396, 1596.25, 1820.493671, 1990.645161, 2091.540541, 2176.137255, 2214.235294, 2254.647059, 2288.105263, 2292.666667, 2298.25, 2293.4, 2298, 2297.375, 2296.75, 1990, 2000, 0, 1990],
            'recordsPerBin': [0, 0, 0, 0, 14, 41, 59, 94, 105, 160, 155, 182, 144, 141, 138, 143, 101, 80, 79, 62, 74, 51, 34, 34, 19, 15, 16, 5, 7, 1, 4, 1, 2, 0, 1],
            'binStatus': [BinStatus.EXCLUDED, BinStatus.EXCLUDED, BinStatus.EXCLUDED, BinStatus.EXCLUDED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.EXCLUDED, BinStatus.MEASURED, BinStatus.EXCLUDED, BinStatus.EXCLUDED, BinStatus.EXCLUDED, BinStatus.EXCLUDED]}
        self.pcMeasured = PowerCurve(self.measuredDict, cutin=4, windSpeedStep=0.5, interpolate=True)

        self.paddedDict = {
            'bin': [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25],
            'binStatus': [BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.MEASURED, BinStatus.EXCLUDED, BinStatus.MEASURED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED, BinStatus.PADDED],
            'meanWindSpeed': [0, 0.5, 1, 1.5, 2, 2.567573, 3.049436, 3.533027, 3.983401, 4.474223, 5.009557, 5.504098, 5.998416, 6.498972, 7.01533, 7.48005, 7.997179, 8.502244, 8.998963, 9.475692, 9.990098, 10.502778, 10.98144, 11.46609, 11.991792, 12.516277, 13.061749, 13.501243, 13.965829, 14.459646, 15.210542, 15.647492, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25],
            'powerInKilowatts': [0, 0, 0, 0, 0, 38.924286, 52.116171, 86.357288, 120.069468, 187.564762, 267.643125, 359.784516, 471.535165, 611.499306, 767.715603, 935.707971, 1183.769231, 1400.960396, 1596.25, 1820.493671, 1990.645161, 2091.540541, 2176.137255, 2214.235294, 2254.647059, 2288.105263, 2292.666667, 2298.25, 2293.4, 2298, 2297.375, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75, 2296.75],
            'recordsPerBin': [0, 0, 0, 0, 0, 14, 41, 59, 94, 105, 160, 155, 182, 144, 141, 138, 143, 101, 80, 79, 62, 74, 51, 34, 34, 19, 15, 16, 5, 7, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.pcPadded = PowerCurve(self.paddedDict)

        self.shortDict = {
            'bin': [0, 1, 2, 3, 4],
            'meanWindSpeed': [0, 1, 2, 3, 4],
            'powerInKilowatts': [0, 0, 2, 18, 56]}
        self.pcShort = PowerCurve(self.shortDict, cutin=2, warranted=True)

    def tearDown(self):
        self.measuredDict = None
        self.powerCurveDict = None
        self.paddedDict = None
        self.pcWarranted = None
        self.pcMeasured = None
        self.pcPadded = None
        self.shortDict = None
        self.pcShort = None

    def test_calculatePowerCoefficients(self):
        radius = 35.5
        self.pcPadded.calculatePowerCoefficients(radius)
        windSpeed = 10
        availablePower = 0.5 * pi * np.power(radius, 2) * np.power(windSpeed, 3) * 1.225
        self.assertEqual(round(self.pcPadded.data.ix[20, 'powerCoefficient'], 2),
                         round(self.pcPadded.data.ix[20, 'powerInKilowatts'] * 1000 / availablePower, 2))

    def test_interpolate(self):
        testBin = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
        testPower = [0,0,0,0,0,0,0,0,0,0,0,2,4,6,8,10,12,14,16,18,20,36,52,68,84,100,116,132,148,164,180,218,256,294,332,370,408,445,484,522,560]

        df = self.pcShort.interpolate(0.1)
        testDict = df.to_dict(orient='list')
        testDict['bin'] = [int(elem*10) for elem in testDict['bin']]
        testDict['meanWindSpeed'] = [int(elem*10) for elem in testDict['meanWindSpeed']]
        testDict['powerInKilowatts'] = [int(elem*10) for elem in testDict['powerInKilowatts']]
        self.assertEqual(testDict['bin'], testBin)
        self.assertEqual(testDict['bin'], testDict['meanWindSpeed'])
        self.assertEqual(testDict['powerInKilowatts'], testPower)

    def test_getPower(self):
        self.assertEqual(self.pcWarranted.getPower(10), 1223.)
        self.assertEqual(self.pcWarranted.getPower(7.54, 2), 522.04)
        self.assertEqual(self.pcWarranted.getPower(7.5375, 2), 522.04)

    def test_padded(self):
        self.maxDiff = 22323
        self.pcTest = self.pcMeasured.padded()
        self.assertEqual(len(self.pcPadded.data.index), len(self.pcTest.data.index))
        self.assertEqual(self.pcPadded.data.index.values[0], self.pcTest.data.index.values[0])
        self.assertEqual(self.pcPadded.data.index.values[-1], self.pcTest.data.index.values[-1])
        self.assertDictEqual(self.pcPadded.data['bin'].to_dict(), self.pcTest.data['bin'].to_dict())
        self.assertDictEqual(self.pcPadded.data['binStatus'].to_dict(), self.pcTest.data['binStatus'].to_dict())
        self.assertDictEqual(self.pcPadded.data['recordsPerBin'].to_dict(), self.pcTest.data['recordsPerBin'].to_dict())
        self.assertDictEqual(self.pcPadded.data['meanWindSpeed'].round(decimals=6).to_dict(),
                             self.pcTest.data['meanWindSpeed'].round(decimals=6).to_dict())
        self.assertDictEqual(self.pcPadded.data['powerInKilowatts'].round(decimals=6).to_dict(),
                             self.pcTest.data['powerInKilowatts'].round(decimals=6).to_dict())

    def test_validated(self):
        testPC = self.pcMeasured.validated()

        self.assertEqual(len(testPC.data[testPC.data['binStatus'] == BinStatus.EXCLUDED]), 8)
        self.assertEqual(len(testPC.data[testPC.data['binStatus'] == BinStatus.MEASURED]), 26)
        self.assertEqual(len(testPC.data[testPC.data['binStatus'] == BinStatus.INTERPOLATED]), 1)
        self.assertTrue(testPC.data.loc[30, 'powerInKilowatts'], 2297.375)

    def test_aepAdded(self):
        annualMeanWindSpeed = 7.5
        testPC = self.pcMeasured.validated().padded().aepAdded(annualMeanWindSpeed)
        print(testPC.data)
        rayleigh_prev = calc.rayleigh(testPC.data.loc[19, 'meanWindSpeed'], annualMeanWindSpeed)
        rayleigh = calc.rayleigh(testPC.data.loc[20, 'meanWindSpeed'], annualMeanWindSpeed)
        aep = 8760 * (rayleigh - rayleigh_prev) * (testPC.data.loc[20, 'powerInKilowatts'] + testPC.data.loc[19, 'powerInKilowatts']) / 2
        self.assertEqual(aep, testPC.data.loc[20, 'aep_7.5'])
