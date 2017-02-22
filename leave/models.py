# Core Django imports
from django.db import models
from django.contrib.auth.models import User


class Leave(models.Model):

    STATUS = (
        (1, 'New'),
        (2, 'Approved'),
        (3, 'Declined'),
    )

    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    leave_days = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)

    class Meta:
        verbose_name_plural = 'Leave Days'
        db_table = 'leave'


class Period(models.Model):

    period = models.PositiveSmallIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Employee(models.Model):

    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    periods = models.ManyToManyField(Period, blank=True)
    leave = models.ManyToManyField(Leave, blank=True)
    start_date = models.DateField(auto_now_add=False)
    leave_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'employee'
