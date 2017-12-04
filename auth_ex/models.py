from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

def validate_name(name):
    if bool(re.search(r"\d", name)):
        raise ValidationError(ul("Imię nie może zawierać cyfr!"), params={"name": name}, )

def validate_surname(surname):
    if bool(re.search(r"\d", surname)):
        raise ValidationError(ul("Nazwisko nie może zawierać cyfr!"), params={"surname": surname}, ) 

class JednOrg(models.Model):
    #id_jedn = models.CharField(max_length=20)
    id = models.CharField(primary_key=True, max_length=11)
    #nazwa = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False)

    def __str__(self):
        return u'{0}'.format(self.nazwa)


class RodzajPracownika(models.Model):
    #nazwa = models.CharField(max_length=45)
    nazwa = models.TextField(db_index=False)
    
    def __str__(self):
        return u'{0}'.format(self.nazwa)


class Pracownik(models.Model):
    #imie = models.CharField(max_length=45)
    imie = models.CharField(max_length=81, validators=[validate_name])
    #nazwisko = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=55, validators=[validate_surname])
    #email = models.EmailField(max_length=45, null=True)
    szkolenie = models.BooleanField(default=False)
    email = models.EmailField(null=True, unique=True)
    #data_zatr = models.DateField(default=datetime.now, blank=True, verbose_name='Data zatr.')
    rodzaj = models.ForeignKey(
        RodzajPracownika, on_delete = models.CASCADE, null=True, verbose_name='rodzaj')
    jedn_org = models.ForeignKey(
        JednOrg,
        on_delete = models.CASCADE,
        null=True,
        verbose_name='Jedn. org.',
        related_name='+'
    )
    login = models.CharField(max_length=45, null=True, unique=True)
    haslo = models.CharField(max_length=45, null=True)
    numer_ax = models.CharField(max_length=6, unique=True, null=True)
    czy_pracuje = models.BooleanField(default=True)
    user = models.OneToOneField(
        User,
        related_name='+',
        on_delete=models.CASCADE,
        default=None)

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
