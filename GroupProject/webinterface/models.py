from django.db import models
from .utils import *

class ProjectManager(models.Manager):
    def getUploadPath(self, filename):
        return '{0}\sitecalibration\{1}'.format(self.title, filename)


class Project(models.Model):

    title = models.CharField(max_length=64, unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    site_calibration_allowed = models.BooleanField(default=False)

    site_calibration_file = models.FileField(upload_to=ProjectManager.getUploadPath)

    @property
    def dataFilePaths(self):
        return printAllFilesInDirectory()

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
