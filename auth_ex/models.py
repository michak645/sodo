from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=20)
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class RodzajPracownika(models.Model):
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Pracownik(models.Model):
    user = models.OneToOneField(
        User,
        related_name='+',
        on_delete=models.CASCADE)
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, null=True)
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
    login = models.CharField(max_length=45, null=True, unique=True)
    haslo = models.CharField(max_length=45, null=True)

    def __str__(self):
        return u'{0} {1}'.format(
            self.imie,
            self.nazwisko
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super().save(args, kwargs)

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
