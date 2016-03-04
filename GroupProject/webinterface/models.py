from django.db import models
from .utils import *
import json

class ProjectManager(models.Manager):
    def getUploadPath(self, filename):
        return '{0}\sitecalibration\{1}'.format(self.title, filename)


class Project(models.Model):

    title = models.CharField(max_length=64, unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    site_calibration_allowed = models.BooleanField(default=False)
    site_calibration_file = models.FileField(upload_to=ProjectManager.getUploadPath)

    # @property
    # def dataFilePaths(self):
    #     return printAllFilesInDirectory()

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class Analysis(models.Model):
    title = models.CharField(max_length=64, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return self.title


class Turbine(models.Model):
    name = models.CharField(max_length=128, blank=False)

    manufacturer = models.CharField(max_length=200)
    model = models.CharField(max_length=120)
    diameter = models.DecimalField(decimal_places=2, max_digits=10)
    hub_height = models.DecimalField(decimal_places=2, max_digits=10)

    bins = models.CharField(max_length=300)
    powerInKillowats = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def setBins(self, data):
        self.bins = json.dumps(data)

    def getBins(self):
        return json.loads(self.bins)

    def setPowerInKillowats(self, data):
        self.powerInKillowats = json.dumps(data)

    def getPowerInKillowats(self):
        return json.loads(self.powerInKillowats)

    def createPowerCurveDict(self):
        powerCurveDict = {
            'bin': self.getBins(),
            'powerInKilowatts': self.getPowerInKillowats()
        }

        return powerCurveDict