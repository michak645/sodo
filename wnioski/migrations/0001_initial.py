# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-27 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_ex', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Zatwierdzony'), ('2', 'Odrzucony'), ('3', 'Przetwarzanie')], default=3, max_length=1, verbose_name='Status')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data')),
            ],
        ),
        migrations.CreateModel(
            name='Obiekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=45)),
                ('opis', models.TextField()),
                ('jedn_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_ex.JednOrg')),
            ],
        ),
        migrations.CreateModel(
            name='PracownicyObiektyUprawnienia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uprawnienia', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Wgląd'), ('2', 'Tworzenie'), ('3', 'Modyfikacja'), ('4', 'Przetwarzanie na serwerze i w biurze'), ('5', 'Przechowywanie'), ('6', 'Usuwanie, niszczenie'), ('7', 'Udostępnianie, powierzanie, przesyłanie')], default='1', max_length=1, verbose_name='Uprawnienia')),
                ('id_obiektu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wnioski.Obiekt')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_ex.Pracownik')),
            ],
        ),
        migrations.CreateModel(
            name='TypObiektu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.CharField(default='Nieznany', max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Wniosek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('typ', models.CharField(choices=[('1', 'Nadanie uprawnień'), ('2', 'Odebranie uprawnień'), ('3', 'Zmiana uprawnień')], default='1', max_length=1, verbose_name='Typ')),
                ('uprawnienia', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Wgląd'), ('2', 'Tworzenie'), ('3', 'Modyfikacja'), ('4', 'Przetwarzanie na serwerze i w biurze'), ('5', 'Przechowywanie'), ('6', 'Usuwanie, niszczenie'), ('7', 'Udostępnianie, powierzanie, przesyłanie')], default='1', max_length=1, verbose_name='Uprawnienia')),
                ('obiekt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.Obiekt')),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownik', to='auth_ex.Pracownik')),
            ],
        ),
        migrations.AddField(
            model_name='obiekt',
            name='typ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wnioski.TypObiektu'),
        ),
        migrations.AddField(
            model_name='historia',
            name='wniosek',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historia', to='wnioski.Wniosek'),
        ),
    ]
