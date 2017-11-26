# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils import timezone
# from django import forms
# from django.forms.widgets import Widget
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as ul
import re


def validate_name(name):
    if bool(re.search(r"\d", name)):
        raise ValidationError(ul("Imię nie może zawierać cyfr!"), params={"name": name}, )

def validate_surname(surname):
    if bool(re.search(r"\d", surname)):
        raise ValidationError(ul("Nazwisko nie może zawierać cyfr!"), params={"surname": surname}, )        

        
class Uprawnienia(models.Model):
    nazwa = models.TextField(unique=True)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=10, unique=True)
    nazwa = models.TextField(unique=True)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class TypObiektu(models.Model):
    nazwa = models.TextField(unique=True)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Obiekt(models.Model):
    nazwa = models.TextField()
    opis = models.TextField()
    typ = models.ForeignKey(TypObiektu, on_delete = models.CASCADE)
    jedn_org = models.ForeignKey(JednOrg, on_delete = models.CASCADE)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class RodzajPracownika(models.Model):
    nazwa = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Pracownik(models.Model):
    imie = models.CharField(max_length=81, validators=[validate_name])
    nazwisko = models.CharField(max_length=55, validators=[validate_surname])
    email = models.EmailField(null=True, unique=True)
    szkolenie = models.BooleanField(default=False)
    login = models.CharField(max_length=45, null=True, unique=True)
    haslo = models.CharField(max_length=45, null=True)
    rodzaj = models.ForeignKey(RodzajPracownika, on_delete = models.CASCADE, null=True, verbose_name='Rodzaj pracownika')
    jedn_org = models.ForeignKey(JednOrg, on_delete = models.CASCADE, null=True, verbose_name='Jednostka organizacyjna')

    def __str__(self):
        return u'{0} {1}'.format(
            self.imie,
            self.nazwisko
        )

    # class Meta:
    #    order_with_respect_to = 'imie'
    '''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Pracownik.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.pracownik.save()
    '''


class WniosekTyp(models.Model):
    typ = models.TextField(unique=True)

    def __str__(self):
        return u'{0}'.format(self.typ)


class Wniosek(models.Model):
    data = models.DateTimeField('Data złożenia', auto_now=True)
    typ = models.ForeignKey(WniosekTyp, on_delete = models.CASCADE, null=True)
    pracownik = models.ForeignKey(Pracownik, on_delete = models.CASCADE, related_name='pracownik', unique=True)
    obiekt = models.ForeignKey(Obiekt, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return u'{0}. {1}, {2}, {3}'.format(
            self.id,
            self.pracownik,
            self.obiekt,
            self.typ
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Historia.objects.get_or_create(
            wniosek=self,
        )


class Historia(models.Model):
    CHOICES_LIST = (
        ('1', 'Przyjęty'),
        ('2', 'Odrzucony'),
        ('3', 'Przetwarzanie'),
    )
    wniosek = models.ForeignKey(Wniosek, on_delete = models.CASCADE, related_name='historia')
    status = models.CharField(
        'Status', max_length=1, choices=CHOICES_LIST, default=3)
    data = models.DateTimeField('Data edycji', auto_now=True)

    def __str__(self):
        return u'{0} {1}'.format(self.wniosek, self.status)
