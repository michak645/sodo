# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from auth_ex.models import JednOrg
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


class WniosekTyp(models.Model):
    typ = models.TextField(unique=True)

    def __str__(self):
        return '{0}'.format(self.typ)


class Wniosek(models.Model):
    data = models.DateTimeField('Data złożenia', auto_now=True)
    typ = models.ForeignKey(WniosekTyp, on_delete = models.CASCADE, null=True)
    user = models.ForeignKey(Pracownik, on_delete = models.CASCADE, related_name='pracownik', unique=True)
    obiekt = models.ForeignKey(Obiekt, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return '{0} do obiektu \'{1}\', dla użytkownika {2}'.format(
            self.typ,
            self.obiekt,
            self.user
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
        return '{0}'.format(self.wniosek)

    def get_status(self):
        return '{0}'.format(self.get_status_display())
