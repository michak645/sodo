# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_auto_20171228_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='obiekty',
            field=models.ManyToManyField(blank=True, null=True, to='wnioski.Obiekt'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='pracownicy',
            field=models.ManyToManyField(blank=True, null=True, to='auth_ex.Pracownik'),
        ),
    ]
