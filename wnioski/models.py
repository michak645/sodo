# -*- coding: utf-8 -*-
from django.db import models
from auth_ex.models import JednOrg, Pracownik
from multiselectfield import MultiSelectField


uprawnienia = (
    ('1', 'Wgląd'),
    ('2', 'Tworzenie'),
    ('3', 'Modyfikacja'),
    ('4', 'Przetwarzanie na serwerze i w biurze'),
    ('5', 'Przechowywanie'),
    ('6', 'Usuwanie, niszczenie'),
    ('7', 'Udostępnianie, powierzanie, przesyłanie'),
)

'''
def get_parent(jedn_org):
    return JednOrg.objects.get(id=jedn_org)[0]

def get_emp(pracownik):
    return "NIEAKTYWNY_" + Pracownik.objects.get(login=pracownik)[0]

def get_emp_for_POU(login):
    return "NIEAKTYWNY_" + Pracownik.objects.get(login=login)[0]
'''


class TypObiektu(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=45, default="Nieznany")

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Obiekt(models.Model):
    nazwa = models.CharField(max_length=45)
    # typ = models.ForeignKey(TypObiektu, on_delete=models.SET_DEFAULT)
    typ = models.ForeignKey(TypObiektu, on_delete=models.CASCADE)
    # jedn_org = models.ForeignKey(JednOrg, on_delete=models.SET(get_parent))
    jedn_org = models.ForeignKey(JednOrg, on_delete=models.CASCADE)
    opis = models.TextField()

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Wniosek(models.Model):
    typy = (
        ('1', 'Nadanie uprawnień'),
        ('2', 'Odebranie uprawnień'),
        ('3', 'Zmiana uprawnień'),
    )
    data = models.DateTimeField('Data', auto_now=True, blank=False)
    typ = models.CharField('Typ', max_length=1, choices=typy, default='1')
    # pracownik = models.ForeignKey(Pracownik, related_name='pracownik',
    # on_delete=models.SET(get_emp))
    pracownik = models.ForeignKey(Pracownik, related_name='pracownik',
                                  on_delete=models.CASCADE)
    obiekt = models.ForeignKey(Obiekt, on_delete=models.CASCADE, null=True)
    uprawnienia = MultiSelectField('Uprawnienia', max_length=1,
                                   choices=uprawnienia, default='1')

    def __str__(self):
        return '{0} - {1}, {2} do \'{3}\''.format(
            self.pracownik,
            self.obiekt,
            self.get_typ_display(),
            self.get_uprawnienia_display(),
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Historia.objects.get_or_create(
            wniosek=self,
        )


class Historia(models.Model):
    CHOICES_LIST = (
        ('1', 'Zatwierdzony'),
        ('2', 'Odrzucony'),
        ('3', 'Przetwarzanie'),
    )
    wniosek = models.ForeignKey(Wniosek, on_delete=models.CASCADE,
                                related_name='historia')
    status = models.CharField('Status', max_length=1,
                              choices=CHOICES_LIST, default=3)
    data = models.DateTimeField('Data', auto_now=True, blank=False)

    def __str__(self):
        return '{0}'.format(self.wniosek)

    def get_status(self):
        return '{0}'.format(self.get_status_display())


class PracownicyObiektyUprawnienia(models.Model):
    # login = models.ForeignKey(Pracownik,
    #                           on_delete=models.SET(get_emp_for_POU))
    login = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    id_obiektu = models.ForeignKey(Obiekt, on_delete=models.CASCADE)
    uprawnienia = MultiSelectField('Uprawnienia', max_length=1,
                                   choices=uprawnienia, default='1')

    def __str__(self):
        return u'{0} {1} {2}'.format(
            self.login,
            self.id_obiektu,
            self.get_uprawnienia_display()
        )
