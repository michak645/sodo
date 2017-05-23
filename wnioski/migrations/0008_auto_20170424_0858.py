# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0007_remove_wniosek_data_zlo'),
    ]

    operations = [
        migrations.AddField(
            model_name='wniosek',
            name='data_zlo',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='data_zatr',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
