from django.db import models


class Turbine(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)

    turbine = models.ForeignKey(Turbine, related_name='turbine', null=True)

    def __str__(self):
        return self.title


class Analysis(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return self.title

