from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=20)
    nazwa = models.CharField(max_length=45)


class RodzajPracownika(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return '{0}'.format(self.nazwa)


class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_zatr = models.DateField(
        default=datetime.now, blank=True, verbose_name='Data zatr.'
    )
    szkolenie = models.BooleanField(default=False)
    rodzaj = models.ForeignKey(
        RodzajPracownika, null=True, verbose_name='rodzaj')
    jedn_org = models.ForeignKey(
        JednOrg,
        null=True,
        verbose_name='Jedn. org.',
        related_name='+'
    )
    numer_ax = models.CharField(max_length=6, unique=True, null=True)
    czy_pracuje = models.BooleanField(default=True)

#     #imie = models.CharField(max_length=45)
#     imie = models.CharField(max_length=81, validators=[validate_name])
#     #nazwisko = models.CharField(max_length=45)
#     nazwisko = models.CharField(max_length=55, validators=[validate_surname])
#     #email = models.EmailField(max_length=45, null=True)
#     szkolenie = models.BooleanField(default=False)
#     email = models.EmailField(null=True, unique=True)
#     #data_zatr = models.DateField(default=datetime.now, blank=True, verbose_name='Data zatr.')
#     rodzaj = models.ForeignKey(
#         RodzajPracownika, on_delete = models.CASCADE, null=True, verbose_name='rodzaj')
#     jedn_org = models.ForeignKey(
#         JednOrg,
#         on_delete = models.CASCADE,

    def __str__(self):
        return u'{0} {1}'.format(
            self.imie,
            self.nazwisko
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super().save(args, kwargs)

