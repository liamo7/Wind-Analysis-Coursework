from unittest import TestCase
from .data import *
from .ppaTypes import *
import os

__author__ = 'Brian'


class TestDatafile(TestCase):
    def setUp(self):
        self.directory = "/home/brian/Data/Testing"
        self.filename = "Python test dirty data.csv"
        self.configFile = "/home/brian/Data/Testing/Python test dirty data.cfg"
        self.datafile = Datafile(self.filename, self.directory, fileType=FileType.COMBINED, columnSeparator=',',
                                 badDataValues=['#VALUE', ])
        self.datafile.addColumn('Anemometer1_Std', 14, ColumnType.WIND_SPEED, ValueType.STANDARD_DEVIATION,
                                measurementHeight=64, instrumentCalibrationSlope=0.04585, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Anemometer1_Avg', 12, ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=64,
                                instrumentCalibrationSlope=0.04585, instrumentCalibrationOffset=0.2529,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer2_Avg', 17, ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=64,
                                instrumentCalibrationSlope=0.04596, instrumentCalibrationOffset=0.2326,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer2_Std', 19, ColumnType.WIND_SPEED, ValueType.STANDARD_DEVIATION,
                                measurementHeight=64, instrumentCalibrationSlope=0.04596, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Anemometer3_Avg', 22, ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=45,
                                instrumentCalibrationSlope=0.04588, instrumentCalibrationOffset=0.2468,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer3_Std', 24, ColumnType.WIND_SPEED, ValueType.STANDARD_DEVIATION,
                                measurementHeight=45, instrumentCalibrationSlope=0.04588, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Anemometer4_Avg', 27, ColumnType.WIND_SPEED, ValueType.MEAN, measurementHeight=27,
                                instrumentCalibrationSlope=0.04595, instrumentCalibrationOffset=0.2312,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0.21)
        self.datafile.addColumn('Anemometer4_Std', 29, ColumnType.WIND_SPEED, ValueType.STANDARD_DEVIATION,
                                measurementHeight=27, instrumentCalibrationSlope=0.04595, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=0.0462, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane1_avg', 48, ColumnType.WIND_DIRECTION, ValueType.MEAN, measurementHeight=62,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=340,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane1_std', 49, ColumnType.WIND_DIRECTION, ValueType.STANDARD_DEVIATION,
                                measurementHeight=62, instrumentCalibrationSlope=1, instrumentCalibrationOffset=340,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane2_avg', 52, ColumnType.WIND_DIRECTION, ValueType.MEAN, measurementHeight=33.2,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=340,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('WindVane2_std', 53, ColumnType.WIND_DIRECTION, ValueType.STANDARD_DEVIATION,
                                measurementHeight=33.2, instrumentCalibrationSlope=1, instrumentCalibrationOffset=340,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp1_avg', 56, ColumnType.TEMPERATURE, ValueType.MEAN, measurementHeight=61,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp1_std', 57, ColumnType.TEMPERATURE, ValueType.STANDARD_DEVIATION,
                                measurementHeight=61, instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH1_avg', 60, ColumnType.RELATIVE_HUMIDITY, ValueType.MEAN, measurementHeight=61,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH1_std', 61, ColumnType.RELATIVE_HUMIDITY, ValueType.STANDARD_DEVIATION,
                                measurementHeight=61, instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp2_avg', 64, ColumnType.TEMPERATURE, ValueType.MEAN, measurementHeight=27.5,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('AirTemp2_std', 65, ColumnType.TEMPERATURE, ValueType.STANDARD_DEVIATION,
                                measurementHeight=27.5, instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH2_avg', 68, ColumnType.RELATIVE_HUMIDITY, ValueType.MEAN, measurementHeight=27.5,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('RH2_std', 69, ColumnType.RELATIVE_HUMIDITY, ValueType.STANDARD_DEVIATION,
                                measurementHeight=27.5, instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('pressure1_avg', 72, ColumnType.PRESSURE, ValueType.MEAN, measurementHeight=60,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Precipitation_avg', 76, ColumnType.RAINFALL, ValueType.QUANTITY, measurementHeight=0,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('relay_on_status_Tot', 80, ColumnType.MINUTE_COUNT, ValueType.QUANTITY,
                                measurementHeight=0, instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('ModemActive_Tot', 81, ColumnType.MINUTE_COUNT, ValueType.QUANTITY, measurementHeight=0,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Power_W_avg', 83, ColumnType.POWER, ValueType.MEAN, measurementHeight=0,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)
        self.datafile.addColumn('Power_std', 85, ColumnType.POWER, ValueType.STANDARD_DEVIATION, measurementHeight=0,
                                instrumentCalibrationSlope=1, instrumentCalibrationOffset=0,
                                dataLoggerCalibrationSlope=1, dataLoggerCalibrationOffset=0)

        self.datafile.addColumnSet('anemometers', ['Anemometer1_avg', 'Anemometer3_avg', 'Anemometer4_avg'])

        self.datafile.loadFromFile()

    def tearDown(self):
        self.datafile = None
        if os.path.exists(self.configFile):
            os.remove(self.configFile)

    def test_addColumn(self):
        self.assertEqual(len(self.datafile.columns), 26)
        self.assertIsInstance(self.datafile.columns[0], Column)

    def test_addColumnSet(self):
        self.assertEqual(len(self.datafile.columnSets['anemometers']), 3)

    def test_loadFromFile(self):
        self.assertAlmostEqual(self.datafile.data.shape, (10, 26))
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer1_Avg'], 3.019)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer1_Std'], 0.418)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer2_Avg'], 3.025)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer2_Std'], 0.433)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer3_Avg'], 2.904)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer3_Std'], 0.467)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer4_Avg'], 2.849)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Anemometer4_Std'], 0.51)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'WindVane1_avg'], 77.47)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'WindVane2_avg'], 77.78)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'WindVane1_std'], 8.02)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'WindVane2_std'], 8.87)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'AirTemp1_avg'], 13.2)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'AirTemp2_avg'], 12.64)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'AirTemp1_std'], 0.053)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'AirTemp2_std'], 0.061)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'RH1_avg'], 90.9)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'RH2_avg'], 90.5)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'RH1_std'], 0.361)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'RH2_std'], 0.368)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'pressure1_avg'], 967)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Precipitation_avg'], 0)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'relay_on_status_Tot'], -600)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'ModemActive_Tot'], -600)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Power_W_avg'], 27628.57)
        self.assertAlmostEqual(self.datafile.data.ix[0, 'Power_std'], 10630.79)

    def test_saveToFile(self):
        if os.path.exists(self.filename):
            os.rename(self.filename, "TEMPXXX.csv")
        # os.remove(self.filename)
        self.datafile.saveToFile()
        self.assertTrue(os.path.exists(self.filename))
        if os.path.exists(self.filename):
            os.remove(self.filename)
            os.rename("TEMPXXX.csv", self.filename)

    def test_saveMetadata(self):
        os.chdir(self.directory)
        if os.path.exists(self.configFile):
            os.remove(self.configFile)
        self.datafile.saveMetadata()

        self.assertTrue(os.path.exists(self.configFile))

        self.datafile = None
        self.datafile = Datafile(self.filename, self.directory, fileType=FileType.COMBINED, columnSeparator=',')
        self.datafile.loadMetadata()

        self.test_addColumn()
        self.test_addColumnSet()

    def test_clean(self):
        self.datafile.clean()
        self.assertEqual(self.datafile.data.shape, (9, 26))

    def test_applyInstrumentCalibrations(self):
        self.datafile.applyInstrumentCalibrations(removeOriginalCalibration=True)
        self.assertAlmostEqual(round(self.datafile.data.iloc[0]['Anemometer1_Avg'], 5), 3.04062)
        self.assertAlmostEqual(round(self.datafile.data.iloc[0]['Anemometer1_Std'], 6), 0.414833)
        self.assertAlmostEqual(round(self.datafile.data.iloc[0]['WindVane1_avg'], 2), 57.47)

    def test_saveAs(self):
        newFile = 'newfile.csv'
        newConfig = newFile.split('.')[0] + ".cfg"
        newPath = self.directory + "/" + newFile
        if os.path.exists(newPath):
            os.remove(newPath)
        self.datafile.saveAs(newFile, self.directory)
        self.assertTrue(os.path.exists(self.directory + "/" + newFile))
        os.remove(newPath)
        os.remove(self.directory + "/" + newConfig)

    # def test_getMeasurementColumnSet(self):
    #     self.fail()
    #
    # def test_getColumnSet(self):
    #     self.fail()
    #
    # def test_addDerivedColumn(self):
    #     self.fail()

    def test_getColumn(self):
        c = self.datafile.getColumn('Anemometer1_Avg')
        self.assertIsInstance(c, Column)
        self.assertTrue(c.name == 'Anemometer1_Avg')


    def test_configFile(self):
        self.assertEqual(self.datafile.configFile(), self.configFile)
