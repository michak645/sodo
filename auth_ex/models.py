from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class JednOrg(models.Model):
    id_jedn = models.CharField(max_length=20)
    nazwa = models.CharField(max_length=45)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


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

    def __str__(self):
        return '{0}'.format(self.user)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Pracownik.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.pracownik.save()
