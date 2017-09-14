# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils import formats
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver


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
    data_zatr = models.DateField(
        default=datetime.now, blank=True, verbose_name='Data zatr.'
    )
    data_zwol = models.DateField(
        null=True, blank=True, verbose_name='Data zwolnienia', default=None
    )
    szkolenie = models.BooleanField(default=False)
    rodzaj = models.ForeignKey(RodzajPracownika, null=True, verbose_name='rodzaj')
    jedn_org = models.ForeignKey(
        JednOrg, null=True, verbose_name='Jedn. org.'
    )
    login = models.CharField(max_length=45, null=True, unique=True)
    haslo = models.CharField(max_length=45, null=True)

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
    typ = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.typ)


class Wniosek(models.Model):
    typ = models.ForeignKey(WniosekTyp, null=True)
    pracownik = models.ForeignKey(Pracownik, related_name='pracownik')
    obiekt = models.ForeignKey(Obiekt, null=True)
    data = models.DateTimeField('Data', auto_now=True, blank=True)

    def __str__(self):
        return u'Wniosek, {0}, data {1}'.format(
            self.pracownik,
            formats.date_format(self.data, "SHORT_DATETIME_FORMAT")
        )

    # def save(self, *args, **kwargs):
    #     is_new = True if not self.id else False
    #     if is_new:
    #         historia = Historia(wniosek=self.id)
    #         historia.save()
    #     super().save(*args, **kwargs)


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
        return u'{0} {1}'.format(self.wniosek, self.status)
