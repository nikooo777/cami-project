# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-13 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_activity_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='context_info',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='timezone',
        ),
        migrations.AddField(
            model_name='measurement',
            name='ok',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
