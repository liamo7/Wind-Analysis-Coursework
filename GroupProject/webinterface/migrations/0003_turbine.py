# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0002_auto_20160224_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turbine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('manufacturer', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=120)),
                ('diameter', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hub_height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bins', models.CommaSeparatedIntegerField(max_length=300)),
                ('powerInKillowats', models.CommaSeparatedIntegerField(max_length=300)),
            ],
        ),
    ]
