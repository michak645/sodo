from django.forms import ModelForm
from .models import (
    Wniosek,
    Obiekt,
    TypObiektu,
)
from django import forms
from auth_ex.models import RodzajPracownika, Pracownik


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ',)


class SearchForm(forms.Form):
    username = forms.CharField(max_length=100)


class ObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )


class TypeForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )


class EditObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )


class EditWniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'pracownik', 'obiekty')


class EditTypObiektuForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )


class ObiektFiltrowanieForm(forms.Form):
    uprawnienia_choices = (
        ('1', 'Wgląd'),
        ('2', 'Tworzenie'),
        ('3', 'Modyfikacja'),
        ('4', 'Przetwarzanie na serwerze i w biurze'),
        ('5', 'Przechowywanie'),
        ('6', 'Usuwanie, niszczenie'),
        ('7', 'Udostępnianie, powierzanie, przesyłanie'),
    )
    jednostka = forms.CharField(max_length=100, required=False)
    pracownik = forms.CharField(max_length=100, required=False)
    uprawnienia = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=uprawnienia_choices,
        required=False,
    )


class ObiektyFiltrowanieForm(forms.Form):
    nazwa = forms.CharField(max_length=100, required=False)
    jednostka = forms.CharField(max_length=100, required=False)
    typ = forms.CharField(max_length=100, required=False)


class PracownicyFiltrowanieForm(forms.Form):
    nazwisko = forms.CharField(max_length=100, required=False)
    jednostka = forms.CharField(max_length=100, required=False)
    numer_ax = forms.CharField(max_length=100, required=False)
    rodzaj = forms.ModelChoiceField(
        queryset=RodzajPracownika.objects.all().order_by('rodzaj'),
        required=False,
    )


class JednostkiFiltrowanieForm(forms.Form):
    nazwa = forms.CharField(max_length=100, required=False)
    czy_labi = forms.BooleanField(required=False)
    parent = forms.CharField(max_length=100, required=False)


class WniosekFiltrowanieForm(forms.Form):
    uprawnienia_choices = (
        ('1', 'Wgląd'),
        ('2', 'Tworzenie'),
        ('3', 'Modyfikacja'),
        ('4', 'Przetwarzanie na serwerze i w biurze'),
        ('5', 'Przechowywanie'),
        ('6', 'Usuwanie, niszczenie'),
        ('7', 'Udostępnianie, powierzanie, przesyłanie'),
    )
    jednostka = forms.CharField(max_length=100, required=False)
    obiekt = forms.CharField(max_length=100, required=False)
    pracownik = forms.CharField(max_length=100, required=False)
    uprawnienia = forms.ChoiceField(
        choices=uprawnienia_choices,
        required=False,
    )
    data = forms.DateTimeField(required=False)


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'login', 'password', 'imie', 'nazwisko', 'email',
            'rodzaj', 'jedn_org', 'numer_ax', 'czy_user'
        )
        widgets = {
            'password': forms.PasswordInput(),
        }
