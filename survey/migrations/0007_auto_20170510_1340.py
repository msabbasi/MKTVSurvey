# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20170507_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='range_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
