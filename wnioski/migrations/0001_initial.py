# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_ex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Przyjęty'), ('2', 'Odrzucony'), ('3', 'Przetwarzanie')], default=3, max_length=1, verbose_name='Status')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data')),
            ],
        ),
        migrations.CreateModel(
            name='Obiekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=45)),
                ('opis', models.CharField(max_length=45)),
                ('jedn_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_ex.JednOrg')),
            ],
        ),
        migrations.CreateModel(
            name='TypObiektu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Uprawnienia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wniosek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('obiekt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.Obiekt')),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownik', to='auth_ex.Pracownik')),
            ],
        ),
        migrations.CreateModel(
            name='WniosekTyp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='wniosek',
            name='typ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.WniosekTyp'),
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
