# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 01:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rumah_sakit', '0002_auto_20170614_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rumahsakit',
            options={'ordering': ('kelas',)},
        ),
    ]
