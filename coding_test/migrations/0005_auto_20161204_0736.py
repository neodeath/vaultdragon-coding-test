# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-04 07:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding_test', '0004_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vdobject',
            old_name='updated',
            new_name='timestamp',
        ),
    ]
