from django.db import models
from django_mysql.models import JSONField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# Create your models here.

# ============ User Information ============
class PersonalUserInfo(models.Model):
    class Meta:
        abstract = True

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    MARITAL_STATUS = (
        ("single", "single"),
        ("married", "married"),
        ("divorced", "divorced"),
        ("widowed", "widowed")
    )

    LANG = (
        ('en', "English"),
        ('ro', "Romanian"),
        ('dk', "Danish"),
        ('pl', "Polish")
    )

    gender = models.CharField(max_length=1, choices=GENDER, default='M', null=True, blank = True)
    marital_status = models.CharField(choices=MARITAL_STATUS, default='married', null=True, blank=True)
    phone = models.CharField(max_length=16, null = True, blank = True)
    address = models.CharField(max_length=256, null = True, blank=True)
    language = models.CharField(choices=LANG, default="en", null = True, blank = True)
    age = models.PositiveIntegerField(max_length=3, null = True, blank = True)
    height = models.PositiveIntegerField(max_length=3, null = True, blank=True)


class UserAccount(PersonalUserInfo):
    class Meta:
        db_table = 'UserAccount'

    ACCOUNT_ROLES = (
        ('end_user', 'End User'),
        ('caregiver', 'Caregiver'),
        ('doctor', 'Doctor')
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    verified_date = models.DateField()
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField()
    # status = models.CharField
    account_role = models.CharField(choices=ACCOUNT_ROLES, default='end_user')

    def __str__(self):
        return "[" + self.account_role + "]" + self.first_name + " " + self.last_name + "; " + "email: " + self.email

    def __unicode__(self):
        return self.__str__()


class Caregiver(UserAccount):
    caretaker = models.ForeignKey(UserAccount, related_name="caregivers")


class HealthProfessional(UserAccount):
    title = models.CharField(max_length=32)
    affiliation = models.CharField(max_length=128)
    specialty = models.CharField(max_length=64)
    patients = models.ManyToManyRel(UserAccount, related_name="doctors")


# We skip defining a model for the UserSession, because this will most likely be in the form of a Django Middleware or
# REST application (e.g. Django-REST-Framework)
# class UserSession(models.Model):
#     pass

# ================ Devices ================
class Device(models.Model):

    DEVICE_TYPES = (
        ("weight", "Weight Measurement"),
        ("blood_pressure", "Blood Pressure Monitor"),
        ("pulse", "Heart Rate Monitor"),
        ("oxymeter", "Oxymeter"),
        ("pedometer", "Step Counter")
    )

    id = models.AutoField(primary_key=True)
    device_type = models.CharField(choices=DEVICE_TYPES, default="weight")
    manufacturer = models.CharField(null = True, blank = True)
    model = models.CharField(max_length=64, null = True, blank = True)
    serial_number = models.CharField(max_length=64)
    activation_date = models.DateTimeField(auto_now=True)

    used_by = models.ManyToManyRel(UserAccount, related_name="used_devices", through="DeviceUsage")

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        users = self.used_by.all()
        return "[" + self.device_type + "] used by: " + users.first_name + " " + users.last_name


class DeviceUsage(models.Model):
    user_account = models.ForeignKey(UserAccount)
    device = models.ForeignKey(Device)
    uses_since = models.DateField(auto_now=True)


class MeasurementService(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, related_name="used_health_services")

    name = models.CharField(max_length=32)
    service_url = models.URLField()

    connection_info = JSONField()


class InterfaceService(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, related_name="used_interface_services")

    name = models.CharField(max_length=32)
    service_url = models.URLField()

    connection_info = JSONField()


# ================ Measurement Information ================
class Measurement(models.Model):
    MEASUREMENTS = (
        ("weight", "Weight Measurement"),
        ("blood_pressure", "Blood Pressure Measurement"),
        ("pulse", "Heart Rate Measurement"),
        ("saturation", "Blood Oxygen Saturation Measurement"),
        ("steps", "Pedometry")
    )

    MEASUREMENT_UNITS = (
        ("no_dim", "No dimension"),
        ("bpm", "Beats Per Minute"),
        ("kg", "kilogram"),
        ("celsius", "Degrees Celsius"),
        ("mmhg", "Pressure in mm Hg")
    )

    @staticmethod
    def validate_precision_range(value):
        if value < 0 or value > 100:
            raise ValidationError(_('%(value) is not a precision within allowed percentage levels: [0, 100]'),
                                  params={'value': value}, )

    id = models.AutoField(primary_key=True)
    measurement_type = models.CharField(choices=MEASUREMENTS, default="weight")

    unit_type = models.CharField(choices=MEASUREMENT_UNITS, default="kg")
    timestamp = models.DateTimeField(auto_now=True)
    precision = models.PositiveIntegerField(max_length=100, default=100, null = True, blank=True,
                                            validators=[validate_precision_range])
    value_info = JSONField()
    user = models.ForeignKey(UserAccount, related_name="health_measurements")
    device = models.ForeignKey(Device, related_name="performed_measurements")

    context_info = JSONField(null=True, blank = True)

    def __str__(self):
        return "[" + self.measurement_type + "] for user: " + self.user.first_name + " " + self.user.last_name + \
               ", taken at: " + self.timestamp

    def __unicode__(self):
        return self.__str__()


# ================ User Activity Information ================
class Activity(models.Model):
    ACTIVITY_TYPE = (
        ("personal", "personal"),
        ("exercise", "exercise"),
        ("medication", "medication"),
        ("measurement", "measurement")
    )

    ACTIVITY_SOURCE = (
        ("self", "self"),
        ("doctor", "doctor"),
        ("caregiver", "caregiver"),
        ("recommendation", "recommendation")
    )


    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount)
    activity_type = models.CharField(choices=ACTIVITY_TYPE, default="personal")

    is_event = models.BooleanField(default=False)
    starts_at = models.DateTimeField(auto_now=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    activity_source = models.CharField(choices=ACTIVITY_SOURCE, default="self")

    times_postponed = models.PositiveSmallIntegerField(default=0)
    last_postponed_time = models.DateTimeField(null=True, blank=True)

    is_recursive = models.BooleanField(default=False)
