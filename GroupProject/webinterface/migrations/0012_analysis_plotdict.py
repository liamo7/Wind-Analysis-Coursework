# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0011_auto_20160424_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='plotDict',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
    ]
