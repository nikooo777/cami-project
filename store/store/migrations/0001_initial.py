# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-11 19:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=64)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('html_link', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('creator', django_mysql.models.JSONField(blank=True, default=dict, null=True)),
                ('calendar_id', models.CharField(max_length=64)),
                ('calendar_name', models.CharField(max_length=64)),
                ('color', django_mysql.models.JSONField(default=dict)),
                ('start', models.BigIntegerField()),
                ('end', models.BigIntegerField()),
                ('recurring_event_id', models.CharField(blank=True, max_length=64, null=True)),
                ('iCalUID', models.CharField(blank=True, max_length=64, null=True)),
                ('reminders', django_mysql.models.JSONField(default=dict)),
                ('activity_type', models.CharField(choices=[(b'personal', b'personal'), (b'exercise', b'exercise'), (b'medication', b'medication'), (b'measurement', b'measurement')], default=b'personal', max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='CaregiverProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('valid_from', models.DateField(default=django.utils.timezone.now)),
                ('valid_to', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_role', models.CharField(choices=[(b'end_user', b'End User'), (b'caregiver', b'Caregiver'), (b'doctor', b'Doctor')], default=b'end_user', max_length=16)),
                ('gender', models.CharField(blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('language', models.CharField(blank=True, choices=[(b'en', b'English'), (b'ro', b'Romanian'), (b'dk', b'Danish'), (b'pl', b'Polish')], default=b'en', max_length=2, null=True)),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caregivers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='caregiver_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(choices=[(b'weight', b'Weight Measurement'), (b'blood_pressure', b'Blood Pressure Monitor'), (b'pulse', b'Heart Rate Monitor'), (b'oxymeter', b'Oxymeter'), (b'pedometer', b'Step Counter')], default=b'weight', max_length=32)),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True)),
                ('model', models.CharField(blank=True, max_length=64, null=True)),
                ('serial_number', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uses_since', models.DateField(auto_now=True)),
                ('access_info', django_mysql.models.JSONField(default=dict)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EndUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('valid_from', models.DateField(default=django.utils.timezone.now)),
                ('valid_to', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_role', models.CharField(choices=[(b'end_user', b'End User'), (b'caregiver', b'Caregiver'), (b'doctor', b'Doctor')], default=b'end_user', max_length=16)),
                ('gender', models.CharField(blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('language', models.CharField(blank=True, choices=[(b'en', b'English'), (b'ro', b'Romanian'), (b'dk', b'Danish'), (b'pl', b'Polish')], default=b'en', max_length=2, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[(b'single', b'single'), (b'married', b'married'), (b'divorced', b'divorced'), (b'widowed', b'widowed')], default=b'married', max_length=16, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='enduser_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalMonitoringService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('service_url', models.URLField()),
                ('access_info', django_mysql.models.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_monitoring_services', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthProfessionalProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('valid_from', models.DateField(default=django.utils.timezone.now)),
                ('valid_to', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_role', models.CharField(choices=[(b'end_user', b'End User'), (b'caregiver', b'Caregiver'), (b'doctor', b'Doctor')], default=b'end_user', max_length=16)),
                ('gender', models.CharField(blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('language', models.CharField(blank=True, choices=[(b'en', b'English'), (b'ro', b'Romanian'), (b'dk', b'Danish'), (b'pl', b'Polish')], default=b'en', max_length=2, null=True)),
                ('title', models.CharField(max_length=32)),
                ('affiliation', models.CharField(max_length=128)),
                ('specialty', models.CharField(max_length=64)),
                ('patients', models.ManyToManyField(related_name='doctors', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_type', models.CharField(choices=[(b'weight', b'Weight Measurement'), (b'blood_pressure', b'Blood Pressure Measurement'), (b'pulse', b'Heart Rate Measurement'), (b'saturation', b'Blood Oxygen Saturation Measurement'), (b'steps', b'Pedometry')], default=b'weight', max_length=32)),
                ('unit_type', models.CharField(choices=[(b'no_dim', b'No dimension'), (b'bpm', b'Beats Per Minute'), (b'kg', b'kilogram'), (b'celsius', b'Degrees Celsius'), (b'mmhg', b'Pressure in mm Hg')], default=b'kg', max_length=8)),
                ('timestamp', models.BigIntegerField()),
                ('timezone', models.CharField(default=b'UTC', max_length=32)),
                ('precision', models.PositiveIntegerField(blank=True, default=100, null=True, validators=[store.models.validate_precision_range])),
                ('value_info', django_mysql.models.JSONField(default=dict)),
                ('context_info', django_mysql.models.JSONField(blank=True, default=dict, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performed_measurements', to='store.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_measurements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='used_by',
            field=models.ManyToManyField(related_name='used_devices', through='store.DeviceUsage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('user', 'calendar_id', 'event_id')]),
        ),
    ]
