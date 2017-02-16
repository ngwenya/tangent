# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 16:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('leave_days', models.PositiveSmallIntegerField()),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_days', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'Approved'), (3, 'Declined')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Leave Days',
                'db_table': 'leave',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='leave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Leave'),
        ),
    ]