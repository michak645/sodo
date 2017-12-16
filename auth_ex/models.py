from django.db import models
from datetime import datetime


class JednOrg(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=11)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    czy_labi = models.BooleanField(default=False)
    nazwa = models.CharField('Nazwa', max_length=255, default="Wydział Matematyki i Informatyki")

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.nazwa)

    def get_ancestor(self):
        return 


class RodzajPracownika(models.Model):
    rodzaj = models.CharField(max_length=255)

    def __str__(self):
        return '{0}'.format(self.rodzaj)


class Pracownik(models.Model):
    login = models.CharField('Login', max_length=15, unique=True, primary_key=True)
    imie = models.CharField('Imie', max_length=90)
    nazwisko = models.CharField('Nazwisko', max_length=90)
    email = models.EmailField('Email', max_length=60)
    # Czy szkolenie jest nam potrzebne? Co to będzie zmieniać w systemie?
    # szkolenie = models.BooleanField(default=False)
    rodzaj = models.ForeignKey(RodzajPracownika, related_name='+', null=True, on_delete=models.CASCADE)
    jedn_org = models.ForeignKey(JednOrg, related_name='+', null=True, on_delete=models.CASCADE)
    numer_ax = models.CharField(max_length=6, unique=True, null=True)

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
    # pracownik = models.OneToOneField(
    #     Pracownik, null=True, blank=True, related_name='pracownik')
    login = models.ForeignKey(Pracownik, 'login')
    jednostka = models.ForeignKey(JednOrg, related_name='+', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.login)


class Drzewo(models.Model):
    labi = models.ForeignKey(Labi, on_delete=models.CASCADE)
    jednostka = models.ForeignKey(JednOrg, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.labi, self.jednostka)