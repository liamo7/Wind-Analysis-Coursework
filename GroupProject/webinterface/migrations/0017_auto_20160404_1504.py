# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0016_auto_20160403_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='directory',
            field=models.CharField(default='E:\\Documents\\Uni\\yr3\\groupproj\\GroupProject', max_length=600),
        ),
    ]
