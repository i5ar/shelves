# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 22:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portables', '0002_auto_20170610_0016'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PortableModel',
            new_name='DownloadModel',
        ),
    ]
