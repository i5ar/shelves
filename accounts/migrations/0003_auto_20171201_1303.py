# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-01 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171128_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='gender',
            field=models.CharField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], default='', max_length=1),
        ),
    ]
