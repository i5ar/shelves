# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-13 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0002_auto_20170810_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='examevent',
            name='submitted',
            field=models.BooleanField(default=False, verbose_name='Submitted'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='examevent',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diaries.RegistrationEvent', verbose_name='Registration'),
        ),
        migrations.AlterField(
            model_name='registrationevent',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Firm'),
        ),
    ]
