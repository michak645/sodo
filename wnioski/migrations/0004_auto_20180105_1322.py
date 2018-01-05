# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-05 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0003_auto_20180105_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wniosek',
            name='komentarz',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='uprawnienia',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Wgląd'), ('2', 'Tworzenie'), ('3', 'Modyfikacja'), ('4', 'Przetwarzanie na serwerze i w biurze'), ('5', 'Przechowywanie'), ('6', 'Usuwanie, niszczenie'), ('7', 'Udostępnianie, powierzanie, przesyłanie')], max_length=1, verbose_name='Uprawnienia'),
        ),
    ]