# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-06 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0006_auto_20180105_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZatwierdzoneObiekty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zatwierdzone', models.BooleanField(default=False, verbose_name='Zatwierdzone przez administratora systemu')),
                ('obiekt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wnioski.Obiekt')),
                ('wniosek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wnioski.Wniosek')),
            ],
        ),
        migrations.AlterField(
            model_name='administratorobiektu',
            name='pracownik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='auth_ex.Pracownik'),
        ),
        migrations.AlterField(
            model_name='historia',
            name='status',
            field=models.CharField(choices=[('1', 'Złożony'), ('2', 'Zatwierdzone przez LABI'), ('3', 'Zatwierdzone przez ABI'), ('4', 'Zatwierdzone przez AS'), ('5', 'Odrzucony')], default=1, max_length=1, verbose_name='Status'),
        ),
    ]
