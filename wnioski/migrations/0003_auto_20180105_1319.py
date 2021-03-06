# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-05 12:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_ex', '0001_initial'),
        ('wnioski', '0002_administratorobiektu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wniosek',
            name='obiekt',
        ),
        migrations.AddField(
            model_name='wniosek',
            name='obiekty',
            field=models.ManyToManyField(related_name='obiekty', to='wnioski.Obiekt'),
        ),
        migrations.AddField(
            model_name='wniosek',
            name='pracownicy',
            field=models.ManyToManyField(help_text='Pracownicy których dotyczy wniosek', related_name='pracownicy', to='auth_ex.Pracownik'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='pracownik',
            field=models.ForeignKey(help_text='Pracownik składający wniosek', on_delete=django.db.models.deletion.CASCADE, related_name='pracownik', to='auth_ex.Pracownik'),
        ),
    ]
