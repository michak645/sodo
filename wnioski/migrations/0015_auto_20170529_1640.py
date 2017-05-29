# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0014_pracownik_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pracownik',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='user',
        ),
        migrations.AddField(
            model_name='pracownik',
            name='haslo',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='login',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
