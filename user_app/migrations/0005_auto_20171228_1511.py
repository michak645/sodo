# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_cart_uprawnienia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='obiekty',
            field=models.ManyToManyField(blank=True, to='wnioski.Obiekt'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='pracownicy',
            field=models.ManyToManyField(blank=True, to='auth_ex.Pracownik'),
        ),
    ]
