from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField, HStoreField
from windAnalysis.powerCurve import *
from math import pi


class Turbine(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False)
    manufacturer = models.CharField(max_length=300, blank=True, null=True)
    model =models.CharField(max_length=300, blank=True, null=True)

    hubHeight = models.FloatField(blank=False, null=False, default=80)
    diameter = models.FloatField(blank=False, null=False, default=90)

    bin = ArrayField(models.FloatField(blank=True, null=True), blank=True, null=True)
    powerInKillowats = ArrayField(models.FloatField(blank=True, null=True), blank=True, null=True)

    # stripeArea = models.FloatField(blank=True, null=True)
    # proportion = models.FloatField(blank=True, null=True)
    # windSpeedHeight = models.FloatField(blank=True, null=True)

    stripes = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def radius(self):
        return self.diameter / 2

    def lowerTipHeight(self):
        return self.hubHeight - self.radius()

    def upperTipHeight(self):
        return self.hubHeight + self.radius()

    def sweptArea(self):
        return pi * pow(self.diameter / 2, 2)

    def getPowerCurveDict(self):
        return {'bin': self.bin, 'powerInKilowatts': self.powerInKillowats}

    def warrantedPowerCurve(self):
        return PowerCurve(self.getPowerCurveDict(), interpolate=True, warranted=True)

    def addOneMetreHorizontalStripes(self):

        self.list = []

        previousHeight = self.lowerTipHeight()
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
            self.list.append({'stripeArea': stripeArea,
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
            self.list.append({'stripeArea': stripeArea,
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
            self.list.append({'stripeArea': stripeArea,
                                 'proportion': proportion,
                                 'windSpeedHeight': windSpeedHeight})


        print(self.list)
        self.stripes = self.list
        self.save()
        print(self.stripes)


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

