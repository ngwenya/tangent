# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 17:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_auto_20170216_1644'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='employee',
            table='employee',
        ),
        migrations.AlterModelTable(
            name='leave',
            table='leave',
        ),
    ]
