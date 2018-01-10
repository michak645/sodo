from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
# from wnioski.models import Obiekt

'''
def get_parent_from_org(parent):
    return JednOrg.objects.get(id=parent)[0]

def get_parent_from_emp(jedn_org):
    return JednOrg.objects.get(id=jedn_org)[0]
'''


class JednOrg(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=11)
    # parent = models.ForeignKey('self', null=True, blank=True,
    #                            on_delete=models.SET(set_parent))
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    czy_labi = models.BooleanField(default=False)
    nazwa = models.CharField('Nazwa', max_length=255, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.nazwa)


# Gdy usuwamy jednostkę organizacyjną to jednostka
# poniżej musi mieć rodzica jako rodzica jednostki,
# która została usunięta
@receiver(pre_delete, sender=JednOrg)
def set_parent(sender, instance, **kwargs):
    parent_id = instance.parent
    JednOrg.objects.filter(parent=instance.id) \
                   .update(parent=parent_id)


class RodzajPracownika(models.Model):
    rodzaj = models.CharField(max_length=255, unique=True, default="Zwykły")

    def __str__(self):
        return '{0}'.format(self.rodzaj)


class Pracownik(models.Model):
    login = models.CharField(
        'Login', primary_key=True, max_length=15, unique=True)
    password = models.CharField(
        'Haslo', max_length=30, null=True, blank=True)
    imie = models.CharField('Imie', max_length=90)
    nazwisko = models.CharField('Nazwisko', max_length=90)
    email = models.EmailField('Email', max_length=60)
    # rodzaj = models.ForeignKey(RodzajPracownika, related_name='+',
    # null=True, on_delete=models.SET_DEFAULT)
    rodzaj = models.ForeignKey(
        RodzajPracownika, related_name='+', null=True,
        on_delete=models.CASCADE
    )
    # jedn_org = models.ForeignKey(JednOrg,
    # related_name='+', null=True, on_delete=models.SET(set_parent))
    jedn_org = models.ForeignKey(
        JednOrg, related_name='+', null=True, on_delete=models.CASCADE)
    numer_ax = models.CharField(max_length=6, unique=True, null=True)
    czy_aktywny = models.BooleanField(default=True)
    czy_user = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.imie, self.nazwisko)

    def name(self):
        return '{} {}'.format(self.imie, self.nazwisko)

    def clean(self):
        if self.czy_user and not self.password:
            raise ValidationError('Password is required')


class Labi(models.Model):
    # login = models.ForeignKey(Pracownik, 'login', on_delete=models.CASCADE)
    login = models.ForeignKey(Pracownik, 'login')
    jednostka = models.ForeignKey(
        JednOrg, related_name='+', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.login.login)
