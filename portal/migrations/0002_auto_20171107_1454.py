# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portal',
            name='user',
            field=models.CharField(max_length=50, verbose_name='User'),
        ),
    ]
