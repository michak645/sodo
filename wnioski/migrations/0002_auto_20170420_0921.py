# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wnioski', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wnioski',
            name='id_prac_sklada',
            field=models.ForeignKey(related_name='wnioski_sklada', default=0, to='wnioski.Pracownicy'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wnioski',
            name='id_prac_dot',
            field=models.ForeignKey(related_name='wnioski_dot', to='wnioski.Pracownicy'),
        ),
    ]
