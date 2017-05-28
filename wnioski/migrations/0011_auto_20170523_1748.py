# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 15:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0010_auto_20170523_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='WniosekTyp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=9)),
            ],
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='data_zatr',
            field=models.DateField(blank=True, default=datetime.datetime.now, verbose_name='Data zatr.'),
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='data_zwol',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data zwolnienia'),
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='jedn_org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.JednOrg', verbose_name='Jedn. org.'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='data_zlo',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Data zło.'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='prac_dot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wnioski_dot', to='wnioski.Pracownik', verbose_name='Dotyczy'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='prac_sklada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wnioski_sklada', to='wnioski.Pracownik', verbose_name='Składający'),
        ),
        migrations.AlterField(
            model_name='wniosek',
            name='typ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.WniosekTyp'),
        ),
    ]
