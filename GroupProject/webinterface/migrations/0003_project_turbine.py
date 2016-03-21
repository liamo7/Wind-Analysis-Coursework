# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0002_turbine'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='turbine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='turbine', to='webinterface.Turbine'),
        ),
    ]