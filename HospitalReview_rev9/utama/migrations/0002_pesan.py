# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pesan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=200)),
                ('isi', models.TextField()),
                ('waktu', models.DateTimeField(auto_now_add=True)),
                ('akun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pesans', to='utama.Akun')),
            ],
            options={
                'ordering': ('-waktu',),
            },
        ),
    ]
