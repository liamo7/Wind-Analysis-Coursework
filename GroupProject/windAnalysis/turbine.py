from math import modf, pi, log10, acos
from .powerCurve import *

__author__ = 'Brian'


class Turbine(object):
    def __init__(self, turbine='Undefined'):
        self.name = turbine
        self.stripes = None
        if turbine == 'Enercon_E70':
            self.manufacturer = 'Enercon'
            self.model = 'E-70'
            self.diameter = 71.0
            self.hubHeight = 64.0
            powerCurveDict = {
                'bin': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
                'powerInKilowatts': [0, 0, 2, 18, 56, 127, 240, 400, 626, 892, 1223.0, 1590.0, 1900.0, 2080.0, 2230.0, 2300.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 2310.0, 0.]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, cutin=2, interpolate=True, warranted=True)
            self.addOneMetreHorizontalStripes()
        elif turbine == 'Siemens SWT-2.3-101':
            self.manufacturer = 'Siemens'
            self.model = 'SWT-2.3-101'
            self.diameter = 100.6
            self.hubHeight = 73.5
            powerCurveDict = {
                'bin': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
                'powerInKilowatts': [0, 0, 0, 0, 113, 234, 431, 708, 1076, 1545, 2015, 2241, 2294, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 2300, 0]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, interpolate=True, warranted=True)
            self.addOneMetreHorizontalStripes()
        elif turbine == 'Nordex N90':
            self.manufacturer = 'Nordex'
            self.model = 'N90'
            self.diameter = 90
            self.hubHeight = 80
            powerCurveDict = {
                'bin': [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25],
                'powerInKilowatts': [0, 0, 0, 0, 0, 0, 0, 29, 76, 136, 207, 292, 390, 504, 635, 787, 958, 1147, 1352, 1570, 1799, 2036, 2231, 2368, 2454, 2496, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]}
            self.warrantedPowerCurve = PowerCurve(powerCurveDict, windSpeedStep=0.5, interpolate=True, warranted=True)
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
        return pi * pow(self.diameter / 2, 2)

    def addOneMetreHorizontalStripes(self):
        previousHeight = self.lowerTipHeight()
        self.stripes = []
        diameterFraction = np.round(self.diameter % 1, 7)
        loopLimit = self.diameter
        if diameterFraction > 0:
            loopLimit = self.diameter - 1
            height = round(previousHeight + diameterFraction / 2, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction / 4, 7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})
            previousHeight = height
        for i in np.arange(loopLimit):
            height = round(previousHeight + 1, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + 0.5, 7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})
            previousHeight = height
        if diameterFraction > 0:
            height = round(previousHeight + diameterFraction / 2, 7)
            upperLimit = height - self.hubHeight
            lowerLimit = previousHeight - self.hubHeight
            stripeArea = calc.stripeArea(self.radius(), lowerLimit, upperLimit)
            proportion = stripeArea / self.sweptArea()
            windSpeedHeight = round(previousHeight + diameterFraction / 4, 7)
            self.stripes.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})


