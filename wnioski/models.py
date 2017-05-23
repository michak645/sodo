from django.db import models
from datetime import datetime
from django.utils import formats
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Uprawnienia(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=20)
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class TypObiektu(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class Obiekt(models.Model):
    nazwa = models.CharField(max_length=45)
    typ = models.ForeignKey(TypObiektu)
    jedn_org = models.ForeignKey(JednOrg)
    opis = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class RodzajPracownika(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class Pracownik(models.Model):
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, null=True)
    data_zatr = models.DateField(default=datetime.now, blank=True)
    data_zwol = models.DateField(null=True, blank=True)
    szkolenie = models.BooleanField(default=False)
    rodzaj = models.ForeignKey(RodzajPracownika, null=True)
    jedn_org = models.ForeignKey(JednOrg, null=True)
    login = models.CharField(max_length=45, null=True)
    haslo = models.CharField(max_length=45, null=True)

    def __unicode__(self):
        return u'{0} {1}'.format(
            self.imie,
            self.nazwisko
        )


class Wniosek(models.Model):
    typ = models.CharField(max_length=9, null=True)
    data_zlo = models.DateTimeField(default=datetime.now, blank=True)
    prac_sklada = models.ForeignKey(Pracownik, related_name='wnioski_sklada')
    prac_dot = models.ForeignKey(Pracownik, related_name='wnioski_dot')
    obiekt = models.ForeignKey(Obiekt)

    def __unicode__(self):
        return u'{0} {1} {2} {3}, {4}'.format(
            self.typ,
            formats.date_format(self.data_zlo, "SHORT_DATETIME_FORMAT"),
            self.prac_sklada,
            self.prac_dot,
            self.obiekt
        )


class Status(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class Historia(models.Model):
    wniosek = models.ForeignKey(Wniosek)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return u'{0} {1}'.format(self.wniosek, self.status)
