from django.db import models
from datetime import datetime


class JednOrg(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True)
    czy_labi = models.BooleanField(default=False)
    opis = models.CharField('Opis', max_length=45)

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.opis)

    def get_ancestor(self):
        return 


class RodzajPracownika(models.Model):
    rodzaj = models.CharField(max_length=45)

    def __str__(self):
        return '{0}'.format(self.rodzaj)


class Pracownik(models.Model):
    imie = models.CharField('Imie', max_length=60)
    nazwisko = models.CharField('Nazwisko', max_length=60)
    email = models.EmailField('Email', max_length=60)
    data_zat = models.DateField('Data zatrudnienia', default=datetime.now, blank=True)
    # Czy szkolenie jest nam potrzebne? Co to będzie zmieniać w systemie?
    # szkolenie = models.BooleanField(default=False)
    rodzaj = models.ForeignKey(RodzajPracownika, related_name='+', null=True)
    jedn_org = models.ForeignKey(JednOrg, related_name='+', null=True)
    numer_ax = models.CharField(max_length=6, unique=True, null=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return u'{0} {1}'.format(
            self.imie,
            self.nazwisko
        )

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         pass
    #     super().save(args, kwargs)


class Labi(models.Model):
    imie = models.CharField('Imie', max_length=60)
    nazwisko = models.CharField('Nazwisko', max_length=60)
    email = models.EmailField('Email', max_length=60)
    jednostka = models.ForeignKey(JednOrg, related_name='+', null=True)

    def __str__(self):
        return 'LABI {0} {1}'.format(self.imie, self.nazwisko)


class Drzewo(models.Model):
    labi = models.ForeignKey(Labi)
    jednostka = models.ForeignKey(JednOrg)

    def __str__(self):
        return '{0} - {1}'.format(self.labi, self.jednostka)