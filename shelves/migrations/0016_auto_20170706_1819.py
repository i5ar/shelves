# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-06 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shelves', '0015_auto_20170706_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelf',
            old_name='numb',
            new_name='nums',
        ),
    ]
