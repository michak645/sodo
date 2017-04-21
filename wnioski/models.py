from django.db import models


class Pracownik(models.Model):
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)

    def __unicode__(self):
        return u'{0} {1}'.format(self.imie, self.nazwisko)


class Obiekt(models.Model):
    nazwa = models.CharField(max_length=40)
    typ = models.CharField(max_length=30)
    jedn_org = models.CharField(max_length=30)
    opis = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0}'.format(self.nazwa)


class Wniosek(models.Model):
    prac_dot = models.ForeignKey(Pracownik, related_name='wnioski_dot')
    prac_sklada = models.ForeignKey(Pracownik, related_name='wnioski_sklada')
    obiekt = models.ForeignKey(Obiekt, on_delete=models.CASCADE)
    data_zlo = models.DateTimeField('date published')
