# -*- coding: utf-8 -*-
from django.db import models
from auth_ex.models import Pracownik, JednOrg


class Uprawnienia(models.Model):
    #nazwa = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False)
    
    def __str__(self):
        return u'{0}'.format(self.nazwa)


class TypObiektu(models.Model):
    #nazwa = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False)
    
    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Obiekt(models.Model):
    #nazwa = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False)
    opis = models.TextField(db_index=False)
    #typ = models.ForeignKey(TypObiektu)
    typ = models.ForeignKey(TypObiektu, on_delete = models.CASCADE)
    #jedn_org = models.ForeignKey(JednOrg)
    jedn_org = models.ForeignKey(JednOrg, on_delete = models.CASCADE)
    #opis = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class WniosekTyp(models.Model):
    #typ = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False, default="Zwykły")
    
    def __str__(self):
        return u'{0}'.format(self.typ)


class Wniosek(models.Model):
    data = models.DateTimeField('Data', auto_now=True, blank=False)
    typ = models.ForeignKey(WniosekTyp, on_delete = models.CASCADE, null=True)
    pracownik = models.ForeignKey(Pracownik, on_delete = models.CASCADE, related_name='pracownik')
    obiekt = models.ForeignKey(Obiekt, on_delete = models.CASCADE, null=True)
    #data = models.DateTimeField('Data', auto_now=True, blank=False)

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
    data = models.DateTimeField('Data', auto_now=True, blank=False)

    def __str__(self):
        return u'{0} {1}'.format(self.wniosek, self.status)
