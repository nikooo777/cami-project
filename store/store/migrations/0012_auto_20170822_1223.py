# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-22 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20170822_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_identifier',
            field=models.CharField(default=uuid.uuid4, max_length=64, unique=True),
        ),
    ]
