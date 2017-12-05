# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from auth_ex.models import JednOrg


class Uprawnienia(models.Model):
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


class WniosekTyp(models.Model):
    typ = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.typ)


class Wniosek(models.Model):
    typ = models.ForeignKey(WniosekTyp, null=True)
    user = models.ForeignKey(User, related_name='user')
    obiekt = models.ForeignKey(Obiekt, null=True)
    data = models.DateTimeField('Data', auto_now=True, blank=False)

    def __str__(self):
        return u'{0}. {1}, {2}, {3}'.format(
            self.id,
            self.user,
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
    wniosek = models.ForeignKey(Wniosek, related_name='historia')
    status = models.CharField(
        'Status', max_length=1, choices=CHOICES_LIST, default=3)
    data = models.DateTimeField('Data', auto_now=True, blank=False)

    def __str__(self):
        return '{0}'.format(self.wniosek)

    def get_status(self):
        return '{0}'.format(self.get_status_display())
