# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumah_sakit', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rumahsakit',
            old_name='kelurahan',
            new_name='jalan',
        ),
        migrations.AddField(
            model_name='rumahsakit',
            name='kelas',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=3, null=True),
        ),
    ]