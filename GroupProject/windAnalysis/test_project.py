from unittest import TestCase
from .project import *
from .turbine import *



class TestProject(TestCase):

    def setUp(self):
        self.directory = '/home/brian/Data/Testing'
        self.filename = "combined.txt"
        self.datafile = Datafile(self.filename, self.directory, fileType=FileType.COMBINED, columnSeparator=',', badDataValues=['#VALUE', ])
        self.datafile.addColumn('Mast - 80m Wind Speed Mean', 2, ColumnType.WIND_SPEED, ValueType.MEAN)
        self.datafile.addColumn('Power mean (kW)', 3, ColumnType.POWER, ValueType.MEAN)
        self.datafile.addColumn('windSpeedBin', 4, ColumnType.WIND_SPEED, ValueType.MEAN)
        self.datafile.loadFromFile()
        self.testProject = Project('test', self.directory)
        self.testProject.defineTurbine(Turbine('Siemens SWT-2.3-101'))

    def tearDown(self):
        self.directory = None
        self.filename = None
        self.datafile = None

    def test_makeMeasuredPowerCurve(self):
        pc = self.testProject.makeMeasuredPowerCurve(self.datafile.data, 'Mast - 80m Wind Speed Mean', 'Power mean (kW)', 'windSpeedBin')
        self.assertEqual(len(pc.data[pc.data['binStatus'] == BinStatus.INTERPOLATED]), 1)
        self.assertTrue(pc.data.loc[40, 'binStatus'], BinStatus.INTERPOLATED)
        self.assertTrue(pc.data.loc[40, 'powerInKilowatts'], 1998.505931)
