from django.db import models
from datetime import date


class Uprawnienia(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=20)
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class TypObiektu(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Obiekt(models.Model):
    nazwa = models.CharField(max_length=45)
    typ = models.ForeignKey(TypObiektu)
    jedn_org = models.ForeignKey(JednOrg)
    opis = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class RodzajPracownika(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Pracownik(models.Model):
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, null=True)
    data_zatr = models.DateField(default=date.today)
    data_zwol = models.DateField(null=True, blank=True)
    szkolenie = models.BooleanField(default=False)
    login = models.CharField(max_length=45, null=True)
    haslo = models.CharField(max_length=45, null=True)
    rodzaj = models.ForeignKey(RodzajPracownika, null=True)
    jedn_org = models.ForeignKey(JednOrg, null=True)

    def __str__(self):
        return u'{0} {1}, {2}, {3}'.format(
            self.imie,
            self.nazwisko,
            self.rodzaj,
            self.jedn_org
        )


class Wniosek(models.Model):
    typ = models.CharField(max_length=9, null=True)
    data_zlo = models.DateTimeField(default=date.today)
    prac_sklada = models.ForeignKey(Pracownik, related_name='wnioski_sklada')
    prac_dot = models.ForeignKey(Pracownik, related_name='wnioski_dot')
    obiekt = models.ForeignKey(Obiekt)

    def __str__(self):
        return u'{0} {1} {2} {3} {4}'.format(
            self.typ,
            self.data_zlo,
            self.prac_sklada,
            self.prac_dot,
            self.obiekt
        )


class Status(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Historia(models.Model):
    wniosek = models.ForeignKey(Wniosek)
    status = models.ForeignKey(Status)

    def __str__(self):
        return u'{0} {1}'.format(self.wniosek, self.status)
