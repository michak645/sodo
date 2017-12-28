# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    replaces = [('user_app', '0001_initial'), ('user_app', '0002_auto_20171228_1204'), ('user_app', '0003_auto_20171228_1213'), ('user_app', '0004_cart_uprawnienia'), ('user_app', '0005_auto_20171228_1511')]

    dependencies = [
        ('auth_ex', '__first__'),
        ('wnioski', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('obiekty', models.ManyToManyField(blank=True, to='wnioski.Obiekt')),
                ('pracownicy', models.ManyToManyField(blank=True, to='auth_ex.Pracownik')),
                ('uprawnienia', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Wgląd'), ('2', 'Tworzenie'), ('3', 'Modyfikacja'), ('4', 'Przetwarzanie na serwerze i w biurze'), ('5', 'Przechowywanie'), ('6', 'Usuwanie, niszczenie'), ('7', 'Udostępnianie, powierzanie, przesyłanie')], default='1', max_length=1, verbose_name='Uprawnienia')),
            ],
        ),
    ]
