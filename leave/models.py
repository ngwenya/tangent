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


class Employee(models.Model):

    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    leave = models.ManyToManyField(Leave, blank=True)
    start_date = models.DateField(auto_now_add=False)
    leave_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'employee'
