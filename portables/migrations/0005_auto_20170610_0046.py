# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portables', '0004_auto_20170610_0042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='downloadmodel',
            old_name='lau',
            new_name='recipient',
        ),
        migrations.AlterField(
            model_name='layoutmodel',
            name='recipient',
            field=models.CharField(max_length=128, verbose_name='Recipient'),
        ),
    ]
