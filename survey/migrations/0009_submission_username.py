# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20170511_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
