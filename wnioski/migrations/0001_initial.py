# Generated by Django 2.1.dev20171202154135 on 2017-12-03 01:48

from django.db import migrations, models
import django.db.models.deletion
import wnioski.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Przyjęty'), ('2', 'Odrzucony'), ('3', 'Przetwarzanie')], default=3, max_length=1, verbose_name='Status')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data edycji')),
            ],
        ),
        migrations.CreateModel(
            name='JednOrg',
            fields=[
                ('id_jedn', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True)),
                ('nazwa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Obiekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField()),
                ('opis', models.TextField()),
                ('jedn_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wnioski.JednOrg')),
            ],
        ),
        migrations.CreateModel(
            name='Pracownik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=81, validators=[wnioski.models.validate_name])),
                ('nazwisko', models.CharField(max_length=55, validators=[wnioski.models.validate_surname])),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('szkolenie', models.BooleanField(default=False)),
                ('login', models.CharField(max_length=45, null=True, unique=True)),
                ('haslo', models.CharField(max_length=45, null=True)),
                ('numer_ax', models.CharField(max_length=6, null=True, unique=True)),
                ('czy_pracuje', models.BooleanField(default=True)),
                ('jedn_org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.JednOrg', verbose_name='Jednostka organizacyjna')),
            ],
        ),
        migrations.CreateModel(
            name='RodzajPracownika',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TypObiektu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Uprawnienia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Wniosek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data złożenia')),
                ('obiekt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.Obiekt')),
                ('pracownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownik', to='wnioski.Pracownik')),
            ],
        ),
        migrations.CreateModel(
            name='WniosekTyp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField(default='Zwykły')),
            ],
        ),
        migrations.AddField(
            model_name='wniosek',
            name='typ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.WniosekTyp'),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='rodzaj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wnioski.RodzajPracownika', verbose_name='Rodzaj pracownika'),
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
