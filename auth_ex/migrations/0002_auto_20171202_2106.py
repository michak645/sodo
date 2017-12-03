# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 20:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_ex', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pracownik',
            name='email',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='haslo',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='imie',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='login',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='nazwisko',
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]