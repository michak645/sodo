import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
from datetime import datetime
from django.utils import formats


class Uprawnienia(models.Model):
    nazwa = models.CharField(max_length=45)
    
    def __unicode__(self):
        return u"%s" % self.nazwa
'''
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''         


class Jednostki_Organizacyjne(models.Model):
    id_jedn = models.CharField(max_length=20)#, primary_key=True)
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u"%s" % self.nazwa
'''    
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''


class Typy_Obiektow_Chronionych(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u"%s" % self.nazwa
'''    
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''


class Obiekty_Chronione(models.Model):
    nazwa = models.CharField(max_length=45)
    typ = models.ForeignKey(Typy_Obiektow_Chronionych)
    jedn_org = models.ForeignKey(Jednostki_Organizacyjne)
    opis = models.CharField(max_length=45)

    def __unicode__(self):
        return u"%s" % self.nazwa
'''    
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''


class Rodzaje_Pracownikow(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u"%s" % self.nazwa
'''    
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''

        
class Pracownicy(models.Model):
    #id = models.CharField(max_length=20, primary_key=True)
    imie = models.CharField(max_length=90)
    nazwisko = models.CharField(max_length=90)
    email = models.EmailField(max_length=45, null=True)
    data_zatr = models.DateField(default=datetime.now, blank=True)
    data_zwol = models.DateField(null=True, blank=True)
    szkolenie = models.BooleanField(default=False)
    login = models.CharField(max_length=45, null=True)
    haslo = models.CharField(max_length=45, null=True)
    rodzaj = models.ForeignKey(Rodzaje_Pracownikow, null=True)
    jedn_org = models.ForeignKey(Jednostki_Organizacyjne, null=True)
    
    def __unicode__(self):
        return u"%s %s, %s, %s" % (self.imie, self.nazwisko, self.rodzaj, self.jedn_org)
'''
    def __str__(self):
        #return '%s %s %s %s' % (self.imie, self.nazwisko, self.rodzaj, self.jedn_org)
        return u'{0} {1}, {2}, {3}'.format(
            self.imie,
            self.nazwisko,
            self.rodzaj,
            self.jedn_org
        )
'''


class Wnioski(models.Model):
    typ = models.CharField(max_length=9, null=True)
    data_zlo = models.DateTimeField(default=datetime.now, blank=True)
    prac_sklada = models.ForeignKey(Pracownicy, related_name='wnioski_sklada')
    prac_dot = models.ForeignKey(Pracownicy, related_name='wnioski_dot')
    obiekt = models.ForeignKey(Obiekty_Chronione)

    def __unicode__(self):
        return u"%s %s %s %s, %s" % (self.typ, formats.date_format(self.data_zlo, "SHORT_DATETIME_FORMAT"), self.prac_sklada, self.prac_dot, self.obiekt)
'''    
    def __str__(self):
        return u'{0} {1} {2} {3}, {4}'.format(
            self.typ,
            formats.date_format(self.data_zlo, "SHORT_DATETIME_FORMAT"),
            self.prac_sklada,
            self.prac_dot,
            self.obiekt
        )
'''


class Statusy(models.Model):
    nazwa = models.CharField(max_length=45)

    def __unicode__(self):
        return u"%s" % self.nazwa
'''    
    def __str__(self):
        return u'{0}'.format(self.nazwa)
'''


class Historie_Wnioskow(models.Model):
    wniosek = models.ForeignKey(Wnioski)
    status = models.ForeignKey(Statusy)
    #PRACOWNICY_id_pracownika = models.ForeignKey(Pracownicy)
    #data = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.wniosek, self.status)
'''    
    def __str__(self):
        return u'{0} {1}'.format(self.wniosek, self.status)
'''

        
class Wnioski_Obiekty_Chronione_Uprawnienia(models.Model):
    WNIOSKI_id_wniosku = models.ForeignKey(Wnioski)
    OBIEKTY_CHRONIONE_id_obiektu = models.ForeignKey(Obiekty_Chronione)
    UPRAWNIENIA_id_uprawnienia = models.ForeignKey(Uprawnienia)
   
   
class Pracownicy_Obiekty_Chronione_Uprawnienia(models.Model):
    PRACOWNICY_id_pracownika = models.ForeignKey(Pracownicy)
    OBIEKTY_CHRONIONE_id_obiektu = models.ForeignKey(Obiekty_Chronione)
    UPRAWNIENIA_id_uprawnienia = models.ForeignKey(Uprawnienia)
   
