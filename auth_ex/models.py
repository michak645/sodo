from django.db import models


class JednOrg(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=11)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE)
    czy_labi = models.BooleanField(default=False)
    nazwa = models.CharField('Nazwa', max_length=255, null=False, blank=False)

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.nazwa)


class RodzajPracownika(models.Model):
    rodzaj = models.CharField(max_length=255)

    def __str__(self):
        return '{0}'.format(self.rodzaj)


class Pracownik(models.Model):
    login = models.CharField('Login', max_length=15, unique=True,
                             primary_key=True)
    imie = models.CharField('Imie', max_length=90)
    nazwisko = models.CharField('Nazwisko', max_length=90)
    email = models.EmailField('Email', max_length=60)
    rodzaj = models.ForeignKey(RodzajPracownika, related_name='+', null=True,
                               on_delete=models.CASCADE)
    jedn_org = models.ForeignKey(JednOrg, related_name='+', null=True,
                                 on_delete=models.CASCADE)
    numer_ax = models.CharField(max_length=6, unique=True, null=True)

    def __str__(self):
        return u'{0} {1}'.format(self.imie, self.nazwisko)


class Labi(models.Model):
    login = models.ForeignKey(Pracownik, 'login')
    jednostka = models.ForeignKey(JednOrg, related_name='+', null=True,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.login.login)
