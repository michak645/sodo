# -*- coding: utf-8 -*-
from django.db import models
from auth_ex.models import JednOrg, Pracownik
from multiselectfield import MultiSelectField
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save


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
def set_parent(jedn_org):
    return JednOrg.objects.get(id=jedn_org)[0]

def get_emp(pracownik):
    return "NIEAKTYWNY_" + Pracownik.objects.get(login=pracownik)[0]

def get_emp_for_POU(login):
    return "NIEAKTYWNY_" + Pracownik.objects.get(login=login)[0]
'''


@receiver(pre_delete, sender=JednOrg)
def set_parent(sender, instance, **kwargs):
    parent_id = instance.parent
    JednOrg.objects.filter(parent=instance.id).update(parent=parent_id)


'''
# Gdy usuwamy pracownika to chcemy mieć to zaznaczone we wniosku
@receiver(pre_delete, sender=Pracownik)
def get_emp(sender, instance, **kwargs):
    Wniosek.objects.filter(pracownik=instance.login).update(pracownik=None)

# Tworzymy nowy wniosek i nadajemy mu pierwszą historię
@receiver(post_save, sender=Wniosek)
def create_first_history(sender, instance, created, **kwargs):
    if created:
        Historia.create(wniosek=instance)

# Jeżeli wniosek o nadanie/odebranie uprawnień zostanie
# rozpatrzony pozytywnie to uaktualniamy tabelę POU
# (PracownicyObiektyUprawnienia) [aktualnie nie działa dla "Zmiana uprawnień"]
@receiver(post_save, sender=Historia)
def update_POU(sender, instance, **kwargs):
    if instance.status == '1' and typ == '1':
        wnioski = Wniosek.objects.get(id=instance.wniosek)
        for wniosek in wnioski:
            PracownicyObiektyUprawnienia.create(
                login=wniosek.pracownik,
                id_obiektu=wniosek.obiekt,
                uprawnienia=wniosek.uprawnienia
            )
    elif instance.status == '1' and typ == '2':
        wnioski = Wniosek.objects.get(id=instance.wniosek)
        for wniosek in wnioski:
            wniosek.objects.filter(id=wniosek.id).delete()
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
    # jedn_org = models.ForeignKey(JednOrg, on_delete=models.SET(set_parent))
    jedn_org = models.ForeignKey(JednOrg, on_delete=models.CASCADE)
    opis = models.TextField()

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Wniosek(models.Model):
    typy = (
        ('1', 'Nadanie uprawnień'),
        ('2', 'Odebranie uprawnień'),
    )
    data = models.DateTimeField('Data', auto_now=True, blank=False)
    typ = models.CharField('Typ', max_length=1, choices=typy, default='1')
    # pracownik = models.ForeignKey(Pracownik, related_name='pracownik',
    # on_delete=models.SET(get_emp))
    pracownicy = models.ManyToManyField(
        Pracownik,
        related_name='pracownicy',
        help_text='Pracownicy których dotyczy wniosek',
    )
    pracownik = models.ForeignKey(
        Pracownik,
        related_name='pracownik',
        help_text='Pracownik składający wniosek',
    )
    obiekty = models.ManyToManyField(
        Obiekt,
        related_name='obiekty',
    )
    uprawnienia = MultiSelectField(
        'Uprawnienia',
        max_length=1,
        choices=uprawnienia,
    )
    # Po co to jest?s
    czy_zmienione = models.BooleanField(default=False)
    komentarz = models.TextField(
        'Komentarz',
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return 'Pracownik: {}, typ: {}, uprawnienia: {}'.format(
            self.pracownik,
            self.get_typ_display(),
            self.get_uprawnienia_display(),
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Historia.objects.get_or_create(
            wniosek=self,
            pracownik=self.pracownik,
        )


class Historia(models.Model):
    CHOICES_LIST = (
        ('1', 'Złożony'),
        ('2', 'Zatwierdzone przez LABI'),
        ('3', 'Zatwierdzone przez ABI'),
        ('4', 'Zatwierdzone przez AS'),
        ('5', 'Odrzucony'),
    )
    wniosek = models.ForeignKey(Wniosek, on_delete=models.CASCADE,
                                related_name='historia')
    status = models.CharField(
        'Status',
        max_length=1,
        choices=CHOICES_LIST,
        default=1,
    )
    data = models.DateTimeField('Data', auto_now=True, blank=False)
    pracownik = models.ForeignKey(
        Pracownik,
        related_name='+',
        null=True,
        blank=True,
    )

    def __str__(self):
        return '{0}'.format(self.wniosek)

    def get_status(self):
        return '{0}'.format(self.get_status_display())

    @classmethod
    def create(cls, wniosek):
        historia = cls(wniosek=wniosek)
        return historia


class PracownicyObiektyUprawnienia(models.Model):
    # login = models.ForeignKey(Pracownik,
    #                           on_delete=models.SET(get_emp))
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

    def get_uprawnienia(self):
        return '{0}'.format(self.get_uprawnienia_display())

    @classmethod
    def create(cls, login, id_obiektu, uprawnienia):
        pou = cls(login=login, id_obiektu=id_obiektu, uprawnienia=uprawnienia)
        return pou


class AdministratorObiektu(models.Model):
    pracownik = models.ForeignKey(
        Pracownik,
        related_name='admin'
    )
    obiekt = models.ForeignKey(
        Obiekt,
        related_name='+',
    )
    aktywny = models.BooleanField(
        'Aktywny',
        default=True,
    )

    def __str__(self):
        return '{}'.format(self.pracownik)


class ZatwierdzonePrzezAS(models.Model):
    wniosek = models.ForeignKey(
        Wniosek,
        related_name='+',
    )
    obiekt = models.ForeignKey(
        Obiekt,
        related_name='+',
    )
    zatwierdzone = models.BooleanField(
        'Zatwierdzone przez administratora systemu',
        default=False,
    )

    def __str__(self):
        return 'Wniosek id: {}, obiekt: {}'.format(
            self.wniosek.id,
            self.obiekt,
        )
