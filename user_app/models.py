from django.db import models
from auth_ex.models import Pracownik
from wnioski.models import Obiekt
from multiselectfield import MultiSelectField


class Cart(models.Model):
    uprawnienia_choices = (
        ('1', 'Wgląd'),
        ('2', 'Tworzenie'),
        ('3', 'Modyfikacja'),
        ('4', 'Przetwarzanie na serwerze i w biurze'),
        ('5', 'Przechowywanie'),
        ('6', 'Usuwanie, niszczenie'),
        ('7', 'Udostępnianie, powierzanie, przesyłanie'),
    )
    typ_choices = (
        ('1', 'Nadanie uprawnień'),
        ('2', 'Odebranie uprawnień'),
    )

    id = models.CharField(max_length=255, primary_key=True)
    pracownicy = models.ManyToManyField(Pracownik, blank=True)
    obiekty = models.ManyToManyField(Obiekt, blank=True)
    uprawnienia = MultiSelectField('Uprawnienia', max_length=25,
                                   choices=uprawnienia_choices)
    typ_wniosku = models.CharField('Typ', max_length=10, choices=typ_choices)

    def __str__(self):
        return '{0}'.format(self.id)
