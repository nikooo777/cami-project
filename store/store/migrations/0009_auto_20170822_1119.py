# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-22 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20170818_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='serial_number',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]