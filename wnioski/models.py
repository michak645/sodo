from django.db import models
from datetime import datetime
from django.utils import formats
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True,
        null=True, related_name='pracownik'
    )
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
    rodzaj = models.ForeignKey(RodzajPracownika, null=True)
    jedn_org = models.ForeignKey(
        JednOrg, null=True, verbose_name='Jedn. org.'
    )
    admin = models.BooleanField(default=False, null=False)

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
    data_zlo = models.DateTimeField(
        default=datetime.now, blank=True, verbose_name='Data zło.'
    )
    prac_sklada = models.ForeignKey(
        Pracownik, related_name='wnioski_sklada', verbose_name='Składający'
    )
    prac_dot = models.ForeignKey(
        Pracownik, related_name='wnioski_dot', verbose_name='Dotyczy'
    )
    obiekt = models.ForeignKey(Obiekt)

    def __str__(self):
        return u'Wniosek, {0}, data {1}'.format(
            self.prac_sklada,
            formats.date_format(self.data_zlo, "SHORT_DATETIME_FORMAT")
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
