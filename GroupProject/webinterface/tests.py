from django.test import TestCase
from .models import *


class TurbineTestCase(TestCase):
    def setUp(self):
        Turbine.objects.create(name="TestCase_Turbine",
                               manufacturer="TestCase_Manufacturer",
                               model="TestCase_Model",
                               bin=[0, 1, 2, 3, 4, 5],
                               powerInKillowats=[0, 1, 2, 3, 4, 5])

    def testCreatedCorrectly(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual(turbine.name, 'TestCase_Turbine')
        self.assertEqual(turbine.manufacturer, 'TestCase_Manufacturer')
        self.assertEqual(turbine.model, 'TestCase_Model')
        self.assertEqual(turbine.bin, [0, 1, 2, 3, 4, 5])
        self.assertEqual(turbine.powerInKillowats, [0, 1, 2, 3, 4, 5])

    def testRadius(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual(turbine.diameter / 2, turbine.radius())
        self.assertNotEqual(turbine.diameter / 2, turbine.radius() + 1)

    def testLowerTipHeight(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual(turbine.hubHeight - turbine.radius(), turbine.lowerTipHeight())
        self.assertNotEqual(turbine.hubHeight - turbine.radius(), turbine.lowerTipHeight() + 1)

    def testUpperTipHeight(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual(turbine.hubHeight + turbine.radius(), turbine.upperTipHeight())
        self.assertNotEqual(turbine.hubHeight + turbine.radius(), turbine.upperTipHeight() + 1)

    def testSweptArea(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual(pi * pow(turbine.diameter / 2, 2), turbine.sweptArea())
        self.assertNotEqual(pi * pow(turbine.diameter / 2, 2), turbine.sweptArea() + 1)

    def testGetPowerCurveDict(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        self.assertEqual({'bin': turbine.bin, 'powerInKilowatts': turbine.powerInKillowats}, turbine.getPowerCurveDict())

    def testWarrantedPowerCurve(self):
        turbine = Turbine.objects.get(name="TestCase_Turbine")
        expectedCurve = PowerCurve(turbine.getPowerCurveDict(), interpolate=True, warranted=True)
        actualCurve = turbine.warrantedPowerCurve()

        self.assertEquals(expectedCurve.cutin, actualCurve.cutin)
        self.assertEquals(expectedCurve.cutout, actualCurve.cutout)
        self.assertEquals(expectedCurve.windSpeedStep, actualCurve.windSpeedStep)
        self.assertEquals(expectedCurve.referenceAirDensity, actualCurve.referenceAirDensity)


class JsonDataFileTestCase(TestCase):
    def setUp(self):
        JsonDataFile.objects.create(name="TestCase_JsonDataFile",
                                    jsonData={'data':'thisIsData'},
                                    projectID=0,
                                    analysisID=0)

    def testCreatedCorrectly(self):
        json = JsonDataFile.objects.get(name="TestCase_JsonDataFile")
        self.assertEqual(json.name, 'TestCase_JsonDataFile')
        self.assertEqual(json.jsonData, {'data':'thisIsData'})
        self.assertEqual(json.projectID, 0)
        self.assertEqual(json.analysisID, 0)


class AnalysisTestCase(TestCase):
    def setUp(self):
        derivedDataFile = JsonDataFile.objects.create(name="TestCase_JsonDataFile",
                                                      jsonData={'data':'thisIsData'},
                                                      projectID=0,
                                                      analysisID=0)
        project = Project.objects.create()
        Analysis.objects.create(title="TestCase_Analysis",
                                description="TestCase_Description",
                                analysisType=0,
                                derivedDataFile=derivedDataFile,
                                project=project)

    def testCreatedCorrectly(self):
        analysis = Analysis.objects.get(title="TestCase_Analysis")
        self.assertEqual(analysis.title, 'TestCase_Analysis')
        self.assertEqual(analysis.description, 'TestCase_Description')
        self.assertEqual(analysis.analysisType, 0)


class ColumnTestCase(TestCase):
    def setUp(self):
        project = Project.objects.create()
        Column.objects.create(name="TestCase_Column",
                              positionInFile=0,
                              columnType=1,
                              valueType=2,
                              instrumentCalibrationSlope=10,
                              instrumentCalibrationOffset=11,
                              dataLoggerCalibrationSlope=12,
                              dataLoggerCalibrationOffset=13,
                              measurementHeight=14,
                              segmentWeighting=15,
                              inferiorLimitHeight=16,
                              superiorLimitHeight=17,
                              segmentHeight=18,
                              project=project)

    def testCreatedCorrectly(self):
        analysis = Column.objects.get(name="TestCase_Column")
        self.assertEqual(analysis.name, 'TestCase_Column')
        self.assertEqual(analysis.positionInFile, 0)
        self.assertEqual(analysis.columnType, ColumnType(1))
        self.assertEqual(analysis.valueType, ValueType(2))
        self.assertEqual(analysis.instrumentCalibrationSlope, 10)
        self.assertEqual(analysis.instrumentCalibrationOffset, 11)
        self.assertEqual(analysis.dataLoggerCalibrationSlope, 12)
        self.assertEqual(analysis.dataLoggerCalibrationOffset, 13)
        self.assertEqual(analysis.measurementHeight, 14)
        self.assertEqual(analysis.segmentWeighting, 15)
        self.assertEqual(analysis.inferiorLimitHeight, 16)
        self.assertEqual(analysis.superiorLimitHeight, 17)
        self.assertEqual(analysis.segmentHeight, 18)



