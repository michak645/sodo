# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0006_auto_20170423_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wniosek',
            name='data_zlo',
        ),
    ]
