# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 12:34
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0022_testdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testdata',
            name='columns',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
