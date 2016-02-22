from __future__ import division
import numpy as np

# Based primarily on Stull (1988), An introduction to boundary layer meteorology. Kluwer
# Page references are provided in comments


class Meteo(object):

    specificGasConstantForDryAir = 287.058  # J/kg.K
    specificHeatOfDryAir = 1005             # J/kg.K

    @staticmethod
    def potentialTemperature(temperatureK, pressureKPa, referencePressureKPa=100):
        # Stull (1988) p. 7
        return temperatureK * (referencePressureKPa/pressureKPa) ** 0.286

    @staticmethod
    def wavenumber(wavelength):
        # Stull (1988) p. 6
        return 2 * np.pi / wavelength

