from __future__ import division

import numpy as np
from scipy.special import cbrt
from math import pi, acos
gasConstantDryAir = 287.05
gasConstantWaterVapour = 461.5


def airDensity(pressureInMillibars, temperatureInDegrees, relativeHumidityInPercent):
    absoluteTemperature = degreeToKelvin(temperatureInDegrees)
    pressure = millibarToPascal(pressureInMillibars)
    relativeHumidity = relativeHumidityInPercent / 100

    return ((pressure / gasConstantDryAir) - relativeHumidity * vapourPressure(absoluteTemperature) * (
        1 / gasConstantDryAir - 1 / gasConstantWaterVapour)) / absoluteTemperature


def availablePowerInWind(windSpeed, referenceAirDensity=1.225, rotorRadius=45):
    return (0.5 * pow(windSpeed, 3) * pi * pow(rotorRadius, 2)) * referenceAirDensity


def bin(row, columnToBin, binWidth=1.0, zeroIsBinStart=True, roundBinBoundaryUp=True, binNameIsBinCentre=True):
    if zeroIsBinStart:
        correction = 0
    else:
        correction = binWidth / 2

    binValue = int((row[columnToBin] - correction) / binWidth) * binWidth + correction

    if not roundBinBoundaryUp and binValue == row[columnToBin]:
        binValue -= binWidth

    if binNameIsBinCentre:
        binValue += binWidth / 2

    return binValue


def siteCorrectedWindSpeed(row, windSpeed, windDirectionBin, factors={}):
    try:
        (slope, offset) = (factors[int(row[windDirectionBin])]['slope'], factors[int(row[windDirectionBin])]['offset'])
    except:
        slope = 1
        offset = 0
    return row[windSpeed] * slope + offset


def chiSquare(row, expected, columnNames=[]):
    values = [row[columnName] for columnName in columnNames]
    # mean = np.average(values)
    # squareError = [(x-mean)**2/mean for x in values]
    squareError = [(x - row[expected]) ** 2 / row[expected] for x in values]
    return np.sqrt(np.sum(squareError))


def circleArea(radius):
    return pi * radius ^ 2


def componentTurbulenceIntensity(row, standardDeviationX, standardDeviationY, windSpeed):
    return np.sqrt(np.power(row[standardDeviationX], 2) + np.power(row[standardDeviationY], 2)) / row[windSpeed]


def degreeToKelvin(degree):
    return degree + 273


def deviation(expectedValue, actualValue):
    if expectedValue == 0:
        return None
    else:
        return (actualValue - expectedValue) / expectedValue


def interpolate(previousValue, nextValue):
    return (previousValue + nextValue) / 2


def meanAbsolutePercentageError(row, expected, columnNames=[]):
    values = [row[columnName] for columnName in columnNames]
    squareError = [(x - row[expected]) / x for x in values]
    return np.sqrt(np.sum(squareError) / len(columnNames))


def millibarToPascal(millibar):
    return millibar * 100


def normalisedPower(power, airDensity, referenceAirDensity=1.225):
    return power * (referenceAirDensity / airDensity)


def normalisedWindSpeed(windSpeed, airDensity, referenceAirDensity=1.225):
    return windSpeed * cbrt(airDensity / referenceAirDensity)


def powerDeviation(row, powerColumn, windSpeedColumn, powerCurve=None):
    expectedValue = powerCurve.getPower(row[windSpeedColumn])
    return deviation(expectedValue, row[powerColumn])


def powerLawPercentageError(row, referenceValue, measuredValue, alpha, refHeight=0.0, testHeight=0.0):
    calculated = row[referenceValue] * np.power((float(testHeight) / float(refHeight)), row[alpha])
    return row[measuredValue] - calculated / row[measuredValue]


def powerLawWindSpeedEstimate(referenceHeight, referenceWindSpeed, exponent, targetHeight):
    return referenceWindSpeed * np.power(targetHeight / referenceHeight, exponent)


def rayleigh(x, mean):
    return 1 - np.exp(-np.pi / 4 * np.power(x / mean, 2))


def residualSumOfSquares(listOfValuePairs):
    squareError = [np.power(value1 - value2, 2) for (value1, value2) in listOfValuePairs]
    return np.sum(squareError)


def residualSumOfSquaresShear(row, referenceWindSpeedColumn, exponentColumn, referenceHeight, columnSet=[]):
    values = [row[column.name] for column in columnSet]
    fit = [powerLawWindSpeedEstimate(referenceHeight, row[referenceWindSpeedColumn], row[exponentColumn],
                                     column.measurementHeight) for column in columnSet]
    return residualSumOfSquares(zip(fit, values))


def rotorEquivalentWindSpeed(row, rewsColumns, hubHeight, hubHeightWindSpeedColumn):
    windSpeedCubed = 0.
    for column in rewsColumns:
        windSpeedCubed += np.power(row[column.name], 3) * column.segmentWeighting
    equivalentWindSpeed = np.power(windSpeedCubed, 1 / 3)

    firstColumnBelowHubHeight = None
    for firstColumnAtOrAboveHubHeight in sorted(rewsColumns, key=lambda c: c.measurementHeight):
        if firstColumnAtOrAboveHubHeight.measurementHeight >= hubHeight:
            break
        else:
            firstColumnBelowHubHeight = firstColumnAtOrAboveHubHeight

    if firstColumnAtOrAboveHubHeight.measurementHeight == hubHeight:
        REWSHubHeightWindSpeed = row[firstColumnAtOrAboveHubHeight]
    else:
        piecewiseExponent = windShearExponentTwoHeights(row[firstColumnBelowHubHeight.name],
                                                        row[firstColumnAtOrAboveHubHeight.name],
                                                        lowerHeight=firstColumnBelowHubHeight.measurementHeight,
                                                        upperHeight=firstColumnAtOrAboveHubHeight.measurementHeight)
        REWSHubHeightWindSpeed = row[firstColumnAtOrAboveHubHeight.name] * np.power(
                hubHeight / firstColumnAtOrAboveHubHeight.measurementHeight, piecewiseExponent)

    return row[hubHeightWindSpeedColumn] * (equivalentWindSpeed / REWSHubHeightWindSpeed)


def rootMeanSquareError(row, expected, columnNames=[]):
    values = [row[columnName] for columnName in columnNames]
    squareError = [(x - row[expected]) ** 2 for x in values]
    return np.sqrt(np.sum(squareError) / len(columnNames))


def segmentArea(radius, chordHeight):
    return np.power(radius, 2) * acos(chordHeight / radius) - chordHeight * np.power(
            (np.power(radius, 2) - np.power(chordHeight, 2)), 0.5)


def shearCorrectedWindSpeed(row, windSpeedColumn, alphaColumn, turbine=None):
    windSpeedCubed = 0.
    for stripe in turbine.stripes:
        windSpeedCubed += np.power(
                (row[windSpeedColumn] * np.power(stripe['windSpeedHeight'] / turbine.hubHeight, row[alphaColumn])), 3) * \
                          stripe['proportion']
    return np.power(windSpeedCubed, 1 / 3)


def simpleRatioNormalisation(value, reference):
    return value / reference


def specificEnergyProduction(row, windSpeedColumn, powerCurve, decimalPlaces=3):
    return powerCurve.getPower(row[windSpeedColumn], decimalPlaces)


def stripeArea(radius, lowerChordHeight, upperChordHeight):
    if (lowerChordHeight < 0) != (upperChordHeight < 0):
        return pi * np.power(radius, 2) - segmentArea(radius, abs(lowerChordHeight)) - segmentArea(radius, abs(
                upperChordHeight))
    else:
        return abs(segmentArea(radius, abs(upperChordHeight)) - segmentArea(radius, abs(lowerChordHeight)))


def turbulenceIntensity(windSpeedMean, windSpeedStandardDeviation):
    return windSpeedStandardDeviation / windSpeedMean


def turbulenceKineticEnergy(row, standardDeviationX, standardDeviationY, standardDeviationZ):
    return 0.5 * (
        np.power(row[standardDeviationY], 2) + np.power(row[standardDeviationX], 2) + np.power(row[standardDeviationZ],
                                                                                               2))


def turbulenceUpperLimit(hubHeightWindSpeed):
    return 0.1 * (1.25 * hubHeightWindSpeed + 6) / hubHeightWindSpeed


def vapourPressure(absoluteTemperature):
    return 0.0000205 * np.exp(0.0631846 * absoluteTemperature)


def wattsToKilowatts(watts):
    return watts / 1000


def windShearExponentPolyfit(row, columnSet):
    heightLogs = [np.log(c.measurementHeight) for c in columnSet]
    speedLogs = [np.log(row[c.name]) for c in columnSet]
    degree = 1
    polyfitResult = np.polyfit(heightLogs, speedLogs, degree)
    return round(polyfitResult[0], 4)


def windShearExponentByPowerLawFit(row, urefColumn, zref, columnSet):
    uref = row[urefColumn]
    squareError = 1000000
    previous = squareError + 1
    previousPrevious = previous
    alpha = -1.
    step = 0.1
    while step > 0.000001:
        while squareError < previous:
            previousPrevious = previous
            previous = squareError
            squareError = 0.
            alpha += step
            for c in columnSet:
                model = powerLawWindSpeedEstimate(zref, uref, alpha, c.measurementHeight)
                squareError += np.power(float(row[c.name]) - model, 2)
        alpha -= 2 * step
        step = step / 10
        squareError = previousPrevious
        previous = squareError + 1
    return alpha


def windShearExponentTwoHeights(lowerWindSpeed, upperWindSpeed, lowerHeight=10.0, upperHeight=10.0):
    return np.log(upperWindSpeed / lowerWindSpeed) / np.log(float(upperHeight) / float(lowerHeight))

