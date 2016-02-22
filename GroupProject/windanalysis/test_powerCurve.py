from unittest import TestCase
from .project import PowerCurve
from math import pi, exp

__author__ = 'Brian'


class TestPowerCurve(TestCase):
    def setUp(self):
        # windspeeds1 = [0, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        # powerValues1 = [0, 0, 2, 18, 56, 127, 240, 400, 626, 892, 1223.00, 1590.00, 1900.00, 2080.00, 2230.00, 2300.00,
        #                 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00]
        powerCurveDict = {'bin': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
                          'powerInKilowatts': [0, 0, 2, 18, 56, 127, 240, 400, 626, 892, 1223.00, 1590.00,
                                               1900.00, 2080.00, 2230.00, 2300.00, 2310.00, 2310.00, 2310.00,
                                               2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00, 2310.00]}
        self.pcWarranted = PowerCurve(powerCurveDict, cutin=2, interpolate=True)

        # self.pcWarranted = PowerCurve(windspeeds1, powerValues1)

    def tearDown(self):
        self.pcWarranted = None

    def test_calculatePowerCoefficients(self):
        self.pcWarranted.calculatePowerCoefficients()
        radius = 35.5
        windSpeed = 10
        availablePower = 0.5 * pi * radius ^ 2 * windSpeed ^ 3 * 1.225
        self.assertAlmostEqual(self.pcWarranted.data.ix[9, 'powerCoefficients'], availablePower)

    def test_aep(self):
        annualMeanWindSpeed = 10.5
        self.pcWarranted.calculateAep(annualMeanWindSpeed)
        windspeed = 9.0
        power = 892.0
        power_prev = 626.
        cumulativeRayleigh = 1 - exp(-0.25 * pi * pow(windspeed / annualMeanWindSpeed, 2))
        cumulativeRayleigh_prev = 1 - exp(-0.25 * pi * pow((windspeed - 1) / annualMeanWindSpeed, 2))
        aep = 8760 * (cumulativeRayleigh - cumulativeRayleigh_prev) * (power + power_prev) / 2
        self.assertAlmostEqual(self.pcWarranted.data.ix[8, 'aep'], aep)

        aep = self.pcWarranted.aep()
        self.assertAlmostEqual(aep, 10394941.85, 2)

    def test_interpolate(self):
        df = self.pcWarranted.interpolate(0.01)
        self.assertEqual(len(df.index), 2501)

    def test_getPower(self):
        self.assertEqual(self.pcWarranted.getPower(10),1223.)
        self.assertEqual(self.pcWarranted.getPower(7.54, 0.01),522.04)
        self.assertEqual(self.pcWarranted.getPower(7.5375, 0.01), 522.04)
