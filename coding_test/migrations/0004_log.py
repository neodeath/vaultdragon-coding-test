# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-27 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding_test', '0003_auto_20161127_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('key', models.TextField()),
                ('data', models.TextField(default='{}')),
                ('action', models.CharField(choices=[('Create', 'CREATE'), ('Update', 'UPDATE')], max_length=6)),
            ],
        ),
    ]
