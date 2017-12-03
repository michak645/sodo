# Generated by Django 2.1.dev20171202154135 on 2017-12-03 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_ex', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pracownik',
            name='szkolenie',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
