from unittest import TestCase
from test_wind.calculation import *
from test_wind.data import *
from test_wind.ppaTypes import *
import pandas as pd

__author__ = 'Brian'

class TestCalculations(TestCase):
    def setUp(self):
        self.datafile = Datafile("C:\PhD\Data\Testing\Python test data.csv",fileType=FileType.COMBINED,columnSeparator=',')
        self.datafile.addColumn('Anemometer1_avg',1,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=64,instrumentCalibrationSlope=0.04585, instrumentCalibrationOffset=0.2529, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer2_avg',2,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=64,instrumentCalibrationSlope=0.04596, instrumentCalibrationOffset=0.2326, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer3_avg',3,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=45,instrumentCalibrationSlope=0.04588, instrumentCalibrationOffset=0.2468, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer4_avg',4,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=27,instrumentCalibrationSlope=0.04595, instrumentCalibrationOffset=0.2312, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer1_std',5,ColumnType.WIND_SPEED,ValueType.STANDARD_DEVIATION,measurementHeight=64,instrumentCalibrationSlope=0.04585, instrumentCalibrationOffset=0.2529, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer2_std',6,ColumnType.WIND_SPEED,ValueType.STANDARD_DEVIATION,measurementHeight=64,instrumentCalibrationSlope=0.04596, instrumentCalibrationOffset=0.2326, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer3_std',7,ColumnType.WIND_SPEED,ValueType.STANDARD_DEVIATION,measurementHeight=45,instrumentCalibrationSlope=0.04588, instrumentCalibrationOffset=0.2468, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer4_std',8,ColumnType.WIND_SPEED,ValueType.STANDARD_DEVIATION,measurementHeight=27,instrumentCalibrationSlope=0.04595, instrumentCalibrationOffset=0.2312, dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('WindVane1_avg',9,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=62,instrumentCalibrationSlope=1, instrumentCalibrationOffset=340, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane2_avg',10,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=33.2,instrumentCalibrationSlope=1, instrumentCalibrationOffset=340, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane1_std',11,ColumnType.WIND_DIRECTION,ValueType.STANDARD_DEVIATION,measurementHeight=62,instrumentCalibrationSlope=1, instrumentCalibrationOffset=340, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane2_std',12,ColumnType.WIND_DIRECTION,ValueType.STANDARD_DEVIATION,measurementHeight=33.2,instrumentCalibrationSlope=1, instrumentCalibrationOffset=340, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp1_avg',13,ColumnType.TEMPERATURE,ValueType.MEAN,measurementHeight=61,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp2_avg',14,ColumnType.TEMPERATURE,ValueType.MEAN,measurementHeight=27.5,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp1_std',15,ColumnType.TEMPERATURE,ValueType.STANDARD_DEVIATION,measurementHeight=61,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp2_std',16,ColumnType.TEMPERATURE,ValueType.STANDARD_DEVIATION,measurementHeight=27.5,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH1_avg',17,ColumnType.RELATIVE_HUMIDITY,ValueType.MEAN,measurementHeight=61,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH2_avg',18,ColumnType.RELATIVE_HUMIDITY,ValueType.MEAN,measurementHeight=27.5,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH1_std',19,ColumnType.RELATIVE_HUMIDITY,ValueType.STANDARD_DEVIATION,measurementHeight=61,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH2_std',20,ColumnType.RELATIVE_HUMIDITY,ValueType.STANDARD_DEVIATION,measurementHeight=27.5,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('pressure1_avg',21,ColumnType.PRESSURE,ValueType.MEAN,measurementHeight=60,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Precipitation_avg',22,ColumnType.RAINFALL,ValueType.QUANTITY,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('relay_on_status_Tot',23,ColumnType.MINUTE_COUNT,ValueType.QUANTITY,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('ModemActive_Tot',24,ColumnType.MINUTE_COUNT,ValueType.QUANTITY,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Power_W_avg',25,ColumnType.POWER,ValueType.MEAN,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Power_std',26,ColumnType.POWER,ValueType.STANDARD_DEVIATION,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WTG_TechAvail_Tot',27,ColumnType.MINUTE_COUNT,ValueType.QUANTITY,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WTG_StormControl_Tot',28,ColumnType.MINUTE_COUNT,ValueType.QUANTITY,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_temp_avg',29,ColumnType.TEMPERATURE,ValueType.MEAN,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_pressure_avg',30,ColumnType.PRESSURE,ValueType.MEAN,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_RH_avg',31,ColumnType.RELATIVE_HUMIDITY,ValueType.MEAN,measurementHeight=0,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS1',32,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=44,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir1',33,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=44,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS2',34,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=53,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir2',35,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=53,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS3',36,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=62,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir3',37,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=62,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS4',38,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=71,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir4',39,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=71,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS5',40,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=80,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir5',41,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=80,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS6',42,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=87,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir6',43,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=87,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_WS7',44,ColumnType.WIND_SPEED,ValueType.MEAN,measurementHeight=97,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('LiDAR_dir7',45,ColumnType.WIND_DIRECTION,ValueType.MEAN,measurementHeight=97,instrumentCalibrationSlope=1, instrumentCalibrationOffset=0, dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.loadFromFile()
        self.datafile.addColumnSet('anemometers', ['Anemometer1_avg', 'Anemometer3_avg', 'Anemometer4_avg'])

    def tearDown(self):
        self.datafile = None
        self.anemometers = None

    def testDegreeToKelvin(self):
        self.assertEqual(degreeToKelvin(0),273)

    def testMillibarToPascal(self):
        self.assertEqual(millibarToPascal(10),1000)

    def testWattsToKilowatts(self):
        self.assertEqual(wattsToKilowatts(1000), 1)

    def testBin(self):
        self.assertEqual(bin(self.datafile.data.iloc[0],'Anemometer1_avg',binWidth=0.5), 3.25, msg="With binWidth=0.5 and defaults, 3.019 should evaluate to 3.25")
        self.assertEqual(bin(self.datafile.data.iloc[0],'Anemometer1_avg',binWidth=0.5, zeroIsBinStart=False), 3.0, msg="With binWidth=0.5 and zeroIsBinStart=False, 3.019 should evaluate to 3.0")
        self.assertEqual(bin(self.datafile.data.iloc[4],'Anemometer1_avg',binWidth=0.5), 3.25, msg="Testing [interval[ 3.0 should evaluate to 3.25")
        self.assertEqual(bin(self.datafile.data.iloc[4],'Anemometer1_avg',binWidth=0.5, roundBinBoundaryUp=False), 2.75, msg="Testing }interval] 3.0 should evaluate to 2.75")
        self.assertEqual(bin(self.datafile.data.iloc[0],'Anemometer1_avg',binWidth=0.5, binNameIsBinCentre=False), 3, msg="When bin name = bin start, 3.019 should evaluate to 3.0")

    def testTI(self):
        self.assertAlmostEqual(turbulenceIntensity(3.0, 0.6), 0.2)

    def testWindShearExponent(self):
        self.assertEqual(windShearExponentPolyfit(self.datafile.data.iloc[0], self.datafile.getColumnSet('anemometers')),2.3616)

    def testRayleigh(self):
        self.assertEqual(rayleigh(0.2,7.5), 0.002232)
        self.assertEqual(rayleigh(5.,7.5), 0.75248)

    def test_availablePowerInWind(self):
        self.assertAlmostEqual(availablePowerInWind(10),3896557)
        self.referenceAirDensity(availablePowerInWind(10, referenceAirDensity=1.0),3180863)
        self.referenceAirDensity(availablePowerInWind(10, referenceAirDensity=1.0, rotorRadius=40),2513274)

    def test_windShearExponentByPowerLawFit(self):
        self.assertAlmostEqual(windShearExponentByPowerLawFit(self.datafile.data.iloc[7],'Anemometer1_avg',64,self.datafile.getColumnSet('anemometers')),0.13227,places=5)
        self.assertAlmostEqual(windShearExponentByPowerLawFit(self.datafile.data.iloc[8],'Anemometer1_avg',64,self.datafile.getColumnSet('anemometers')),-0.04196,places=5)
